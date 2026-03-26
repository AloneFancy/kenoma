# KENOMA · بایگانی دو راستی · Claude Code Project Context

> "When the birds are gone, the good bow is put away. When the hare is dead, the hunting dog is cooked."
> — Fan Li · Eastern Zhou Chronicles · The game's thesis

## What This Game Is

**KENOMA** (The Archive of Two Truths) is a fixed-camera psychological horror tragedy built in Unity 6 URP. A scholar (the 士 archetype — a wandering intellectual who cannot stop serving) enters a sealed Achaemenid Persian archive and is **exactly good enough to be used completely**. The Vanguard — a 300-year-old intelligence who identified this specific Scholar three years before they arrived — has been building a behavioral model of the Scholar since Day One. When the model is complete, the Scholar's work is done. The ending is not a betrayal. It is a completion.

**No game has shipped this mechanic before.** This is why KENOMA exists.

## Project Structure

```
Assets/
├── Scripts/
│   ├── BMS/                    # Behavioral Model System — build first, touch carefully
│   │   ├── BMSController.cs    # Singleton. The spine of everything.
│   │   ├── BMSEvent.cs         # Event types (12 total)
│   │   └── WarmthRegister.cs   # Per-Vanguard warmth tracking
│   ├── Vanguard/
│   │   ├── VanguardStateController.cs  # 5 recognition stages
│   │   ├── VanguardAI.cs               # Utility Score + route prediction
│   │   └── VanguardDialogue.cs         # State-keyed lines
│   ├── Scholar/
│   │   ├── ScholarController.cs
│   │   ├── TDSController.cs    # Translation Depth System (deep-read vs skim)
│   │   ├── FireVessel.cs       # Oil economy + flame VFX
│   │   └── Astrolabe.cs        # Resonance detector (no HUD — all physical)
│   ├── World/
│   │   ├── WorldManager.cs     # Current world, traversal debt
│   │   ├── TraversalFocalPoint.cs
│   │   ├── ObeliskController.cs
│   │   └── BoundaryManager.cs
│   ├── Systems/
│   │   ├── USS/                # Utility Score System — build LAST
│   │   ├── TCS/                # Terrain Control System
│   │   └── SRS/                # Scenario Resolution System (reads BMS at Act III)
│   └── Audio/
│       ├── DarkVoiceController.cs   # Binaural FMOD — spatial origin per line
│       └── ResonanceAudioSystem.cs  # Diegetic status (no HUD)
├── Scenes/
│   ├── Demo_ResonanceObelisk.unity  # Current primary scene
│   └── Prototype_BMS.unity          # BMS integration test scene
└── Design/                          # Design documents (HTML)
    └── kenoma_compact_context.html  # The compact context cluster
```

## The Four Iron Laws — Never Break These

**These are not preferences. Breaking any one makes the game something that already exists.**

1. **Never make the turn a betrayal.** VA tells the Scholar (Clause 18) exactly what is about to happen and walks away to execute it. The turn is a completion.
2. **Never break the Iron Rule.** Knowledge from World B enables action in World A. Material from World A changes World B physically. One rule. Everywhere. Always. If a puzzle design requires bending the rule, the puzzle changes.
3. **Never show the Behavioral Model.** No UI, no "your choice has been remembered," no score counter. The player reads the BMS through one channel: the Vanguard's observed behavior changes.
4. **Never make a puzzle without an author.** Every puzzle exists because a real person made a real decision in that space. Ask: who was here, what did they need, what did they leave?

## System Build Order (Engineering Must Follow This)

```
BMS (SYS-01) → RSS (SYS-02) → TDS (SYS-03) → TVS (SYS-04)
→ RES (SYS-05) → TCS (SYS-07) → SRS (SYS-08) → USS (SYS-06)
```

**BMS first. USS last.** USS requires RSS, TDS, and TVS stable before building.

## The BMS — The Most Critical System

`BMSController` is a singleton that:
- Records 12 event types batched **per room-session** (not per frame)
- Maintains `wa_warmth` and `vb_warmth` registers (ints, clamped −20 to +20)
- **NEVER exposes warmth registers to any UI element**
- Pushes updates to `VanguardStateController` on every record
- Reads by `SRS` at Act III for scenario resolution

**The BMS register is only readable by Vanguard behavior systems. Never by the player.**

## The Vanguard — Five Recognition Stages

Both Vanguards run through 5 stages driven by accumulated BMS data:
- **S1** — Asks questions (needs information)
- **S2** — Stops asking methodology (knows Scholar's methods)
- **S3** — Anticipates / pre-stages resources
- **S4** — Answers before Scholar finishes asking
- **S5 ⚠** — Already knows. Observing only. **Most dangerous stage. Model is complete.**

Stage transitions are observable through behavior changes only — never announced.

## The Iron Rule (Crossing System)

- Every crossing increments `traversalDebt` (int on `WorldManager`)
- Boundary manifests: Debt 2 = 8 sec, Debt 3 = 20 sec, Debt 4+ = persistent until save
- Vanguard **never crosses**. Debt = 0 for both Vanguards always.
- The Scholar pays all crossing costs. This asymmetry is visible from minute one.

## Audio Architecture — Non-Negotiable

**Dark Voice is binaural, not reverb.** FMOD with HRTF. Every Dark Voice line has a specified spatial origin:
- **Behind** = suppressed thought surfacing against Scholar's will
- **Beside** = strategic analysis running in parallel
- **Ahead** = warning about what Scholar is about to do

World A acoustic identity: warm brass harmonics, fire altar crackle, floor resonance channels.
World B acoustic identity: near-silence, Scholar's fire vessel = only sound anchor, cold stone resonance.

**Zero HUD.** All status is physical:
- Oil level = fire vessel flame VFX scale
- Creature proximity = astrolabe ring vibration
- Scholar health = robe damage + posture degradation

## Coding Conventions

- All Unity MonoBehaviours use `[RequireComponent]` where dependencies exist
- Events dispatched through static event systems (not `GetComponent` chains)
- BMS events are `struct BMSEvent` — value types, batched in `List<BMSEvent>` per session
- Vanguard AI never uses NavMesh GetPath directly — always through `VanguardAI.RequestMove()`
- No magic strings — all BMS event tags are `const string` in `BMSEventTags.cs`
- FMOD events are `const string` paths in `AudioPaths.cs`

## Key Design References

| System | Reference Game | What It Proves |
|--------|---------------|----------------|
| Fixed cameras | AitD Trilogy / TNN | Architecture shapes dread |
| Invisible tracking | Silent Hill 2 | BMS must surface through behavior |
| Crossing cost | PoP: Warrior Within | The Dahaka pursues consequence, not malice |
| Zero HUD | Metro 2033 | Status is more frightening when physical |
| Adaptive antagonist | Hello Neighbor (⚠ failure) | Vanguard predicts one move ahead — never mirrors |

## What "Done" Looks Like for the Demo

One playtester verdict only: **"The Vanguard treated me differently based on what I chose."**

If testers describe only their own actions ("I chose to help one side"), the BMS is running but not surfacing through behavior. That is a failure state.

## Available Custom Commands

| Command | Does |
|---------|------|
| `/iron-check` | Verifies current file against all four Iron Laws |
| `/bms-event` | Scaffolds a new BMS event type with correct fields |
| `/new-puzzle` | Scaffolds a puzzle — enforces Iron Law IV (must have author) |
| `/vanguard-dialogue` | Writes Vanguard dialogue in correct voice and stage register |
| `/dark-voice` | Writes Dark Voice lines with binaural spatial origin specified |
| `/crossing-logic` | Generates traversal focal point crossing code |
| `/consequence-table` | Generates BMS consequence table for a solution set |
| `/scene-review` | Reviews current Unity scene against KENOMA design principles |
| `/creature-naming` | Generates Naming combat sequence for a creature type |
| `/demo-check` | Runs the full demo verification checklist |

## Available Agents

| Agent | Invoke When |
|-------|-------------|
| `narrative-guardian` | Before merging any system that touches Vanguard behavior or puzzle design |
| `bms-architect` | Designing or modifying the BMS event schema or warmth register logic |
| `unity-systems` | Implementing any of the 8 core systems |
| `playtester` | Simulating player experience to catch design failures before building |

## Document Authority (When Design and Code Conflict)

Story always beats production. If a systems document and a story document disagree:
1. Storytelling Bible v8 (source of truth)
2. Complete Narrative + Phase Design Doc
3. Game Loop & Systems
4. GDD v5

The outer ring changes. The inner ring does not.
