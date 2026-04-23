---
description: Scaffold the Vessel Sacrifice puzzle (PZ-WA-011) — the KENOMA reinvention of Prince of Persia 2's "He Who Would Steal the Flame Must Die." Enforces puzzle authorship (Archivist Shirin), Iron Rule compliance, and the BMS event with largest single warmth delta for VB.
---

This command scaffolds the complete Vessel Sacrifice puzzle at Shirin's Threshold (WB, near WB-004 junction). The puzzle is pre-authored — Archivist Shirin's backstory is canonical and must not be changed. You may adapt room details, camera composition, Lantern-Thief patrol schedules, and tablet content.

---

## Canonical Puzzle Header

```csharp
// PUZZLE ID: PZ-WA-011
// ROOM: WB — SHIRIN_THRESHOLD (between WB-004 junction and WB-∞ approach)
// PUZZLE AUTHOR: Archivist Shirin, junior cataloger, original Archive staff
// ORIGINAL PURPOSE: To protect the Previous Scholar's final journal entry — the
//   one that named what the Archive had always been intended to do. Shirin found
//   it, understood it, and could not decide whether to hide it or share it.
//   She hid it behind her own worst fear: complete darkness. She wanted only
//   someone who had chosen darkness voluntarily to read what she left.
// CURRENT STATE: 300 years later, the threshold mechanism still works. The
//   inscription is still legible. The tablet is still there. The darkness is
//   still absolute.
// IRON RULE: Scholar sacrifices fire vessel warmth (World A material/resource)
//   to gain access to Shirin's tablet (World B knowledge). The act of extinguishing
//   is the material input. The knowledge in the darkness is the output. Iron Rule: ✓
```

---

## Solution States

**Solution Path A — The Scholar Extinguishes:**
The Scholar reads the inscription, understands what it requires, and extinguishes their fire vessel voluntarily. They navigate 14 seconds of darkness to reach Shirin's tablet. They read it. When they exit, Lantern-Thieves that were circling now follow them at distance — the Scholar's warmth residue is a new signal they haven't processed before. The Scholar must reignite at the nearest fire altar.

*BMS consequence:*
```csharp
BMSController.Instance.RecordEvent(new BMSEvent {
    eventType           = BMSEventType.VesselSacrifice,
    tag                 = BMSEventTags.VESSEL_SACRIFICE,
    wa_warmthDelta      = +4,
    vb_warmthDelta      = +8,
    roomId              = RoomIDs.WB_THRESHOLD_SHIRIN,
    sessionTime         = sessionTimer,
    wasVanguardObserved = VanguardObservationSystem.IsVanguardNear(RoomIDs.WB_THRESHOLD_SHIRIN),
    phase               = PhaseManager.CurrentPhaseTag
});
```

*Vanguard observable behavior after Solution A:*
- VA: begins providing patrol routes that avoid areas where Lantern-Thieves now behave anomalously — she has updated her Scholar-risk model without being asked
- VB: in her next interaction, she quotes a single phrase from Shirin's tablet without attribution, as if she has always known it — she is testing whether the Scholar read it

**Solution Path B — The Scholar Does Not Extinguish:**
The Scholar reads the inscription and turns away. Shirin's tablet remains unread. The Previous Scholar's final entry remains unknown. No BMS event fires.

*Long-term consequence:* In high-score endings, VB references this tablet in the Child Phase. The Scholar who never read it hears a phrase without context. The Scholar who read it on a second attempt understands the full weight. The absence is the most significant gap in the Scholar's keystoneGaps profile.

*This is not failure.* The Scholar chose not to enter the darkness. That is a character choice. The keystoneGap is data.

**There is no Path C for this puzzle.** Some puzzles have only two states: you chose or you didn't. This is one of them.

---

## C# Scaffold — VesselSacrificeController.cs

```csharp
// PUZZLE ID: PZ-WA-011 — Shirin's Threshold
// PUZZLE AUTHOR: Archivist Shirin, junior cataloger
// ORIGINAL PURPOSE: Protection of final Previous Scholar journal entry through fear
// CURRENT STATE: Threshold intact, mechanism functional, tablet preserved
// IRON RULE: Fire vessel extinguishment (WA material) → Shirin's knowledge (WB)

[RequireComponent(typeof(AudioSource))]
public class VesselSacrificeController : BasePuzzleController
{
    [PuzzleID("PZ-WA-011")]

    [Header("Threshold")]
    [SerializeField] private BoxCollider  thresholdBlocker;   // blocks passage while lit
    [SerializeField] private Transform    shirinTabletAnchor; // position of Shirin's tablet
    [SerializeField] private float        darknessWindowSec = 14f;

    [Header("Lantern-Thief Response")]
    [SerializeField] private float        residualWarmthRadius = 8f; // post-extinguish tracking range
    [SerializeField] private LanternThief[] patrollingThieves;

    [Header("Audio")]
    [SerializeField] private FMODEventRef thresholdHumAmbient;       // AudioPaths.SHIRIN_THRESHOLD_HUM
    [SerializeField] private FMODEventRef extinguishSuccessSound;    // AudioPaths.VESSEL_EXTINGUISH_VOLUNTARY
    [SerializeField] private FMODEventRef darknessAmbient;           // AudioPaths.WB_ABSOLUTE_DARK

    [Header("Debug — DISABLE BEFORE SHIP")]
    [SerializeField] private bool debugMode = false;

    private bool _puzzleResolved = false;
    private float _darknessTimer = 0f;

    private void OnEnable()
    {
        FireVessel.OnVesselExtinguished += HandleVesselExtinguished;
    }

    private void OnDisable()
    {
        FireVessel.OnVesselExtinguished -= HandleVesselExtinguished;
    }

    // Scholar voluntarily extinguishes at threshold
    // Called ONLY by FireVessel.cs — not by this controller
    private void HandleVesselExtinguished(bool isVoluntary, string roomId)
    {
        if (roomId != RoomIDs.WB_THRESHOLD_SHIRIN) return;
        if (!isVoluntary) return;  // forced extinguish (Lantern-Thief) does not count
        if (_puzzleResolved) return;

        // FIRE BMS EVENT — largest VB warmth event in game
        // Fires AFTER extinguish animation, BEFORE darkness phase begins
        BMSController.Instance.RecordEvent(new BMSEvent {
            eventType           = BMSEventType.VesselSacrifice,
            tag                 = BMSEventTags.VESSEL_SACRIFICE,
            wa_warmthDelta      = +4,
            vb_warmthDelta      = +8,
            roomId              = RoomIDs.WB_THRESHOLD_SHIRIN,
            sessionTime         = sessionTimer,
            wasVanguardObserved = VanguardObservationSystem.IsVanguardNear(roomId),
            phase               = PhaseManager.CurrentPhaseTag
        });

        // Open threshold
        thresholdBlocker.enabled = false;

        // Begin darkness phase
        StartCoroutine(DarknessPhase());
    }

    private IEnumerator DarknessPhase()
    {
        // Shift Lantern-Thief behavior: residual warmth tracking
        foreach (var thief in patrollingThieves)
            thief.SetTrackingMode(LanternThiefMode.ResidualWarmth, residualWarmthRadius);

        // Play darkness ambient
        FMODUnity.RuntimeManager.PlayOneShot(darknessAmbient);

        // 14-second window
        yield return new WaitForSeconds(darknessWindowSec);

        // Return Lantern-Thief behavior to normal if Scholar has not exited
        // (Scholar who stayed longer than the window — this is contemplative rhythm data)
        foreach (var thief in patrollingThieves)
            thief.SetTrackingMode(LanternThiefMode.LightTracking);
    }

    // Called when Scholar reaches Shirin's tablet in darkness
    public void OnShirinTabletRead()
    {
        _puzzleResolved = true;
        TDSController.Instance.MarkTabletRead(TabletIDs.SHIRIN_FINAL_ENTRY, isDeepRead: true);

        if (debugMode)
            Debug.Log("[PZ-WA-011] Shirin's tablet read. Keystonegap cleared.");
    }
}
```

---

## Audio Notes

**Threshold ambient (before approach):** A low, resonant hum that is neither warm nor cold — it is neutral. The Archive breathes here differently. It has been waiting.

**At extinguish:** The fire vessel goes out with a sound that is too quiet. Not dramatic. The Scholar made the sound smaller by choosing it. Silence follows — absolute silence for 1.3 seconds before the darkness ambient begins.

**Darkness ambient:** Near-total silence. The Scholar's own breathing. Distant stone resonance. No creature sounds — the Lantern-Thieves are responding to residual warmth, not sound, and their motion is muffled.

**On relight (fire altar after puzzle):** The fire vessel catches with unusual warmth — the altar seems almost eager. This is not mechanical. This is VB's world responding to the Scholar who passed through its darkest threshold.

---

## Dark Voice Lines

```
DARK VOICE — Scholar first reads Shirin's threshold inscription

LINE 1: "The inscription is not a warning. It is an instruction."
ORIGIN: Beside
TIMING: Scholar reads the threshold inscription
ACT REGISTER: I / II

LINE 2 (if Scholar hesitates 4+ seconds): "Fan Li left the kingdom. He did not leave the archive."
ORIGIN: Behind
TIMING: Scholar stands still after reading inscription
ACT REGISTER: I — the voice is noting the Scholar's hesitation

LINE 3 (if Scholar turns away without extinguishing):
"The flame is not protection. It is location."
ORIGIN: Beside
TIMING: Scholar moves away from threshold
ACT REGISTER: II — pure analytical observation, no judgment
```

---

## Shirin's Inscription (at threshold)

*Translation header: Administrative notation. Undated. Irregular script — written under stress or in poor light.*

**Threshold inscription (skim-readable in 5 seconds):**
> "He who would steal the flame from the Dark Archive must first surrender it."

**Shirin's tablet (Shirin's final entry — deep-read content, 25–40 seconds):**
> *"I found the founder's record on the forty-first day. I read it in the light of my oil lamp, which I was burning too quickly because I was frightened. The record names what this archive was always intended to do, and why someone is always standing in each of its worlds. I understood it.*
>
> *I do not know whether to hide this or share it. If I hide it, the next Scholar who comes here and reads it will have faced the dark to find it, and they will understand it the way I did not: from the inside.*
>
> *I am going to hide it. I am going to hide it behind the thing I fear most, which is the absolute dark, which this place has in abundance.*
>
> *I wrote this in the dark. I could not see my own hands. I stayed until it was done. The next Scholar who reads this will also have stayed.*"

**Scholar's murmur (TDS VO — plays during deep-read):**
> *"She was afraid. She did this afraid. She hid the most important thing she had ever found behind her own worst fear, and she wanted someone who had faced the same fear willingly to find it."*

---

## The No-Correct-Answer Clarification

There are two paths: the Scholar entered the darkness or they did not. Neither is marked as correct. A Scholar who chose not to extinguish the vessel is not wrong — they are a different person. The keystoneGap of Shirin's tablet is character data, not failure data. In the Child Phase, VB uses this gap differently for different Scholars.

The puzzle does not offer a "third path" or a "clever alternative." Shirin designed one way in. That is what she left.
