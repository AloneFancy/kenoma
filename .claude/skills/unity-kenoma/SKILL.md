# Unity KENOMA Skill
# Loaded by: unity-systems agent, bms-architect agent, scene-review command
# Purpose: Unity 6 URP patterns, architecture conventions, and system wiring rules for KENOMA

---

## Project Tech Stack

- **Engine:** Unity 6 (6000.0.x LTS)
- **Render Pipeline:** Universal Render Pipeline (URP)
- **Audio Middleware:** FMOD Studio (binaural, spatial audio, world mix switching)
- **AI / NavMesh:** Unity NavMesh + custom Vanguard prediction layer
- **Input:** Unity Input System (new)
- **Version Control:** Git (branch per system sprint)

---

## Architecture Principles

### 1 — Static Events for Cross-System Communication
Never use `GetComponent` chains for system-to-system communication. All cross-system signals go through static events:

```csharp
// Define in the owning system
public static event Action<VanguardSide, int> OnRecognitionStageChanged;
public static event Action<WorldSide> OnWorldSwitched;
public static event Action<SolutionPath> OnPuzzleSolved;

// Subscribe in dependent systems — always unsubscribe in OnDestroy
private void OnEnable()  => BMSController.OnWarmthUpdated += HandleWarmthUpdate;
private void OnDisable() => BMSController.OnWarmthUpdated -= HandleWarmthUpdate;
```

### 2 — Singletons Are Explicit
Use explicit singleton pattern with Instance null-check. No `FindObjectOfType` in production code:

```csharp
public class BMSController : MonoBehaviour
{
    public static BMSController Instance { get; private set; }
    private void Awake()
    {
        if (Instance != null && Instance != this) { Destroy(gameObject); return; }
        Instance = this;
        DontDestroyOnLoad(gameObject);
    }
}
```

### 3 — No Magic Strings
All BMS event tags, FMOD event paths, room IDs, and animation state names are `const string` in dedicated constant files:

```csharp
// BMSEventTags.cs
public static class BMSEventTags
{
    public const string DEEP_READ_COMPLETE      = "DeepReadComplete";
    public const string VOLUNTARY_CROSSING      = "VoluntaryCrossing";
    public const string PUZZLE_SOLVED_SIDED_VA  = "SOLVED_SIDED_VA";
    public const string PUZZLE_SOLVED_SIDED_VB  = "SOLVED_SIDED_VB";
    public const string PUZZLE_SOLVED_UNIFIED   = "SOLVED_UNIFIED";
    // ... all 12 event types
}

// AudioPaths.cs
public static class AudioPaths
{
    public const string DARK_VOICE_BESIDE       = "event:/DarkVoice/Beside";
    public const string DARK_VOICE_BEHIND       = "event:/DarkVoice/Behind";
    public const string DARK_VOICE_AHEAD        = "event:/DarkVoice/Ahead";
    public const string OBELISK_WA_PARTIAL      = "event:/Obelisk/WA_Partial";
    public const string OBELISK_WA_COMPLETE     = "event:/Obelisk/WA_Complete";
    public const string WORLD_SWITCH_TO_WB      = "event:/Transition/ToHollow";
    public const string WORLD_SWITCH_TO_WA      = "event:/Transition/ToFire";
}

// RoomIDs.cs
public static class RoomIDs
{
    public const string WA_001 = "WA-001";
    public const string WA_003 = "WA-003";
    public const string WB_004 = "WB-004";
    public const string WB_INF = "WB-INF";
    // ...
}
```

### 4 — SerializeField for All Designer-Tunable Values

```csharp
[Header("BMS Thresholds")]
[SerializeField] private int[] recognitionStageThresholds = { 3, 6, 10, 16, 22 };

[Header("Utility Score")]
[SerializeField] private float va_executionThreshold = 20f;
[SerializeField] private float vb_executionThreshold = 20f;

[Header("Traversal Debt")]
[SerializeField] private int boundaryDread_debt   = 2;   // 8s Boundary
[SerializeField] private int boundaryPursue_debt  = 3;   // 20s Boundary
[SerializeField] private int boundaryPersist_debt = 4;   // until save
```

### 5 — RequireComponent for Hard Dependencies

```csharp
[RequireComponent(typeof(NavMeshAgent))]
[RequireComponent(typeof(VanguardDialogue))]
public class VanguardStateController : MonoBehaviour { ... }
```

---

## Camera System (Fixed Camera — AitD Model)

```csharp
public class CameraManager : MonoBehaviour
{
    [SerializeField] private CameraPosition[] waPositions;   // 3 per WA room
    [SerializeField] private CameraPosition[] wbPositions;   // 3 per WB room

    // Trigger volumes drive camera switches — not player distance
    // Each camera position has a TriggerVolume child that activates it
    // Cameras never lerp or follow — they cut or crossfade (0.15s max)

    public void SwitchWorld(WorldSide side)
    {
        // Disable all cameras from previous world set
        // Enable default camera for new world set
        // Swap FMOD audio mix
        FMODUnity.RuntimeManager.GetBus("bus:/WorldA").setVolume(
            side == WorldSide.WA ? 1f : 0f);
        FMODUnity.RuntimeManager.GetBus("bus:/WorldB").setVolume(
            side == WorldSide.WB ? 1f : 0f);
    }
}

[System.Serializable]
public struct CameraPosition
{
    public Camera camera;
    public BoxCollider activationVolume;
    public bool framesScholar;       // does this frame show Scholar?
    public bool framesVanguard;      // does this frame show Vanguard?
    public bool framesKeyObject;     // does this frame show the puzzle object?
}
```

---

## World Switching (2.2s Non-Interruptable)

```csharp
public IEnumerator ExecuteCrossing(WorldSide destination)
{
    // Disable player input
    ScholarController.Instance.SetInputEnabled(false);

    // Crossing animation (Scholar steps through ring — 2.2s)
    yield return crossingAnimator.PlayAndWait("TFP_Cross");

    // Swap world roots
    worldA_Root.SetActive(destination == WorldSide.WA);
    worldB_Root.SetActive(destination == WorldSide.WB);

    // Fire vessel VFX: dims on WB entry
    FireVessel.Instance.SetWorldModifier(
        destination == WorldSide.WB ? 0.6f : 1.0f);

    // Camera switch
    CameraManager.Instance.SwitchWorld(destination);

    // Audio mix switch
    AudioManager.Instance.SwitchWorldMix(destination);

    // Re-enable input
    ScholarController.Instance.SetInputEnabled(true);

    // Fire event
    OnWorldSwitched?.Invoke(destination);
}
```

---

## FMOD Integration Patterns

```csharp
// Dark Voice — binaural, spatial origin required
public class DarkVoiceController : MonoBehaviour
{
    // Each line has a spatial origin: Behind / Beside / Ahead
    public void PlayLine(DarkVoiceLine line)
    {
        var instance = FMODUnity.RuntimeManager.CreateInstance(line.fmodPath);

        // Set spatial origin parameter (mapped in FMOD Studio to HRTF position)
        instance.setParameterByName("SpatialOrigin", (float)line.origin);

        // 3D position: binaural derived from listener position + origin offset
        instance.set3DAttributes(
            FMODUnity.RuntimeUtils.To3DAttributes(GetOriginPosition(line.origin)));

        instance.start();
        instance.release();
    }

    private Vector3 GetOriginPosition(DarkVoiceOrigin origin) => origin switch
    {
        DarkVoiceOrigin.Behind => Camera.main.transform.position
                                  - Camera.main.transform.forward * 0.3f,
        DarkVoiceOrigin.Beside => Camera.main.transform.position
                                  + Camera.main.transform.right * 0.25f,
        DarkVoiceOrigin.Ahead  => Camera.main.transform.position
                                  + Camera.main.transform.forward * 0.4f,
        _ => Camera.main.transform.position
    };
}

[System.Serializable]
public struct DarkVoiceLine
{
    public string fmodPath;           // const from AudioPaths.cs
    public DarkVoiceOrigin origin;    // Behind / Beside / Ahead
    public BMSEventType triggerEvent; // fires when this BMS event is recorded
    public int actRegister;           // 1 or 2 (affects FMOD reverb send)
}

public enum DarkVoiceOrigin { Behind, Beside, Ahead }
```

---

## Vanguard NavMesh — Prediction Model

```csharp
// Vanguard never mirrors Scholar's last move — she predicts next move
public class VanguardAI : MonoBehaviour
{
    private NavMeshAgent agent;
    private BMSController bms;

    // Predict Scholar's next room based on behavioral model
    // NOT: "Scholar just went to WA-003, go to WA-003"
    // YES: "Scholar-as-modeled tends to move to resources after combat — pre-position at WA-002 resource cache"
    private string PredictScholarNextRoom()
    {
        var recentEvents = bms.GetRecentEvents(5);
        // Analyze movement pattern from BMS session data
        // Return predicted room ID
        // Default to Scholar's statistically most-visited room type if no pattern
    }

    public void RequestMove(string targetRoomId)
    {
        // Always routes through this method — never direct NavMesh.CalculatePath
        var dest = RoomManager.GetRoomCenter(targetRoomId);
        agent.SetDestination(dest);
    }
}
```

---

## Zero HUD — Physical Status Rules

All game state must be readable from the scene without any UI overlay:

| Game State | Physical Expression | Implementation |
|------------|---------------------|----------------|
| Oil level | FireVessel flame VFX scale (0.2–1.0) | `ParticleSystem.main.startSizeMultiplier` |
| Scholar health | Robe damage material progression (4 states) | Material swap via `Renderer.material` |
| Creature proximity | Astrolabe ring vibration speed + amplitude | Animator float parameter driven by distance |
| Scholar exhaustion | Posture degradation + hand tremor | Animator blend tree |
| World identity | Lighting color temperature + audio mix | URP Volume + FMOD bus |
| Traversal debt pressure | Boundary ambient grow (below hearing then above) | FMOD parameter on Boundary emitter |

**Never add a UI element for any of these.** If a system needs to communicate state, find the physical expression.

---

## Inspector Organization

All MonoBehaviours use `[Header]` to organize the Inspector. Standard groupings:

```csharp
[Header("=== SYSTEM REFERENCES ===")]
[Header("BMS")]
[Header("Warmth / Recognition")]
[Header("Utility Score (USS)")]
[Header("Audio")]
[Header("VFX")]
[Header("Debug — DISABLE BEFORE SHIP")]
```

The Debug header section is always last and always contains a `[SerializeField] bool debugMode` that gates all `Debug.Log` calls. No Debug.Log in production paths.

---

## Git Branch Conventions

```
main            — stable demo build only
dev             — integration branch
sprint/bms      — BMS system sprint
sprint/rss      — Recognition Stage System sprint
sprint/demo-obelisk — Resonance Obelisk demo scene
sprint/vanguard-a-ai — VA state machine implementation
sprint/vanguard-b-ai — VB state machine implementation
```

Merge to dev only after `/scene-review` passes. Merge to main only after `/demo-check` passes.
