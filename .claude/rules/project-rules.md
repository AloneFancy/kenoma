# KENOMA Project Rules
# Applied to every Claude Code session in this project

---

## Rule 1 — BMS Data Is Never Exposed to the Player

The `wa_warmth` and `vb_warmth` registers exist inside `BMSController` only. They are never:
- Referenced in any UI component
- Logged to console in production code paths
- Passed to any system other than `VanguardStateController`
- Used to trigger any player-facing feedback (sound, haptic, visual)

**If you are about to write code that exposes BMS data to anything a player could observe directly — stop. Ask whether the information can be conveyed through Vanguard behavior instead.**

---

## Rule 2 — Never Use Inline Strings for BMS Tags

All BMS event tags are `const string` in `BMSEventTags.cs`. Never write:

```csharp
// WRONG
tag = "DeepReadComplete"

// CORRECT
tag = BMSEventTags.DEEP_READ_COMPLETE
```

Same applies to FMOD event paths (use `AudioPaths.cs`) and room IDs (use `RoomIDs.cs`).

---

## Rule 3 — No BMS Events in Update Loops

BMS events are dispatched once, on completion of an action. Never in `Update()`, `FixedUpdate()`, `LateUpdate()`, or any continuous loop. If a behavior is continuous (Scholar sustaining fire vessel in combat), record a single event at the end of the sustained action, not per-frame.

---

## Rule 4 — The Iron Rule Has No Exceptions

When implementing any puzzle, crossing, or mechanic that involves both worlds: knowledge flows from World B to World A, material flows from World A to World B. If an implementation requires crossing logic that deviates from this even once, the implementation changes. The rule does not.

Run `/iron-check` before committing any file in `Scripts/World/` or `Scripts/Systems/`.

---

## Rule 5 — Vanguard Adapts Through Prediction, Not Mirroring

The Vanguard AI never responds to the Scholar's *last action*. She positions based on her model's prediction of the Scholar's *next action*. This is the difference between the Hello Neighbor failure mode (predictable, felt like a tracking system) and a 300-year intelligence.

```csharp
// WRONG — mirrors last move
agent.SetDestination(scholarLastPosition);

// CORRECT — predicts next move
var predictedRoom = ai.PredictScholarNextRoom();
agent.RequestMove(predictedRoom);
```

---

## Rule 6 — Every Puzzle Must Have An Author

Before implementing any puzzle mechanic, the following must be answered in a comment at the top of the puzzle's controller file:

```csharp
// PUZZLE AUTHOR: [Who built this mechanism in the Archive's history]
// ORIGINAL PURPOSE: [What it was designed to do]
// CURRENT STATE: [What the Scholar finds 300 years later]
// IRON RULE: [How World A ↔ World B information exchange applies]
```

If these four fields cannot be filled in, the puzzle design is incomplete and should not be implemented yet.

---

## Rule 7 — Dark Voice Is Binaural From Day One

Dark Voice lines are FMOD events with spatial origin parameters. They are never:
- Implemented as reverb sends on the Scholar's VO bus
- Played as 2D audio sources
- Added in post-production as an afterthought

Every new Dark Voice line must have its `DarkVoiceOrigin` specified (Behind / Beside / Ahead) at the time it is added to the line bank.

---

## Rule 8 — All Designer-Tunable Values Are SerializeField

No gameplay values are hardcoded. Warmth thresholds, utility score limits, traversal debt thresholds, resource quantities, recognition stage breakpoints — all `[SerializeField]` with a `[Header]` grouping them in the Inspector. Default values are set in-code; they are not the final values.

---

## Rule 9 — Debug Code Is Always Gated

All `Debug.Log` calls are gated behind `if (debugMode)` where `debugMode` is a `[SerializeField] bool` in a dedicated `[Header("Debug — DISABLE BEFORE SHIP")]` section. No Debug.Log in production code paths. The demo build is always built with all debug flags false.

---

## Rule 10 — Story Authority Over System Authority

When a system implementation conflicts with a story document — even when the system implementation is already built — the system changes. The authority hierarchy:

1. Storytelling Bible v8
2. Complete Narrative + Phase Design Doc  
3. Game Loop & Systems
4. Implementation

Use the `narrative-guardian` agent before merging any system that touches Vanguard behavior or puzzle design.
