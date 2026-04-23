# KENOMA · بایگانی دو راستی · Claude Code Project Context

> "When the birds are gone, the good bow is put away. When the hare is dead, the hunting dog is cooked."
> — Fan Li · Eastern Zhou Chronicles · The game's thesis

> "Man must be surpassed."
> — Nietzsche · Thus Spoke Zarathustra · The Scholar's arc

## What This Game Is

**KENOMA** (The Archive of Two Truths) is a fixed-camera psychological horror tragedy built in Unity 6 URP. A scholar (the 士 archetype — a wandering intellectual who cannot stop serving) enters a sealed Achaemenid Persian archive and is **exactly good enough to be used completely** by two competing intelligences who need each other's destruction.

The Vanguards — two people in their **late 20s to mid-30s** who entered the Archive years before the Scholar and have been shaped by their separate worlds — are not guides. They are competitors in a 300-year territorial war. Both need a complete Scholar model because **a complete behavioral model grants its builder traversal capability**: the ability to cross between worlds that neither can currently access alone. The Scholar does not know this. The Scholar never knows this.

**Neither world is the main world. Both are equally real. Both Vanguards are equally the enemy.**

**No game has shipped this mechanic before.** This is why KENOMA exists.

---

## The Man in the High Castle Mechanic

Philip K. Dick: within the losing world, a hidden book describes the world where the winners won. Both exist simultaneously.

In KENOMA: within each world exists a hidden truth about why the Vanguard truly needs the Scholar. Each Vanguard appears to serve the Archive. Each is actually competing to be the one who gains traversal capability — and eliminates the other.

- **VA uses the Scholar** to complete the Archive's administrative record (Clause 18). Once the model is complete and the Scholar is eliminated, VA gains traversal. She crosses to World B. The 300-year war ends.
- **VB uses the Scholar** to access the Third Record — the Archive's founding secret. Once the Scholar unlocks it, VB gains the knowledge to traverse. She crosses to World A. The 300-year war ends differently.
- **The Scholar** is the instrument by which one Vanguard destroys the other. Which one, is determined by the Scholar's behavioral choices — never by any stated allegiance.

The Chamber of Convergence (WB-∞) is the "High Castle" — the place where both truths exist simultaneously and are legible only to someone who has read both worlds completely. The Scholar who reaches it understands everything. They reach it at the moment their use is complete.

---

## Nietzsche's Three Metamorphoses — The Game's Phase Architecture

From *Thus Spoke Zarathustra*: the spirit becomes a camel, then a lion, then a child.

**Phase I — The Camel:** "Thou shalt." The Scholar arrives burdened, eager to serve. Every deep-read, every donation, every crossing is an act of willing submission to the Archive's weight. The camel kneels to take on the heaviest load. *This is the Scholar choosing to be the bow.*

**Phase II — The Lion:** "I will." The Scholar encounters the great dragon — "Thou shalt" — and must fight it. The Lion Phase begins when the Scholar's utility drops below threshold. The Vanguard who reaches her execution threshold first declares Clause 18 and pursues. The Scholar who understood the Fan Li aphorism and continued anyway becomes the Lion. The Scholar who never understood is simply caught.

**Phase III — The Child:** Act III. The surviving Vanguard moves through the Archive alone. This is the child — innocent, creative, new beginning. She did not triumph. She completed. The archive is hers now. She walks north.

**These three phases are not metaphors. They are the game's literal structure. Every system serves one phase.**

---

## The "He Who Would Steal the Flame" Puzzle Mechanic

Reinvented from *Prince of Persia 2: The Shadow and the Flame*.

The original: an inscription warns that stealing the flame means death. The player must let their shadow-self be consumed to pass.

**KENOMA reinvention — The Vessel Sacrifice (PZ-WA-011):**
The Scholar finds an inscription at a threshold: *"He who would steal the flame from the dark archive must first surrender it."* To gain passage (and the knowledge beyond), the Scholar must **voluntarily extinguish their fire vessel** — their primary survival tool, the only warm light in World B, the thing that everything in the dark archive tracks.

Walking through the threshold in darkness, the Scholar is vulnerable for 14 seconds. Lantern-Thieves can see them only by residual warmth. The knowledge on the other side cannot be gained any other way.

**What this teaches:** The fire vessel is not a resource — it is the Scholar's identity in the dark. Giving it up voluntarily is the act that distinguishes the Scholar who serves from fear from the Scholar who serves from understanding.

**BMS consequence:** Largest single warmth event for VB (+8). Significant for VA (+4). This action, more than any other, completes both behavioral models rapidly. Both Vanguards know who this Scholar is the moment they extinguish the flame voluntarily.

The puzzle author: a junior archivist who feared the dark and hid the most important tablet behind her own greatest fear. She wanted only someone who had faced the same fear to read what she left.

---

## Project Structure

```
Assets/
├── Scripts/
│   ├── BMS/
│   │   ├── BMSController.cs        # Singleton. The spine of everything.
│   │   ├── BMSEvent.cs             # 12 event types + wasVanguardObserved flag
│   │   ├── WarmthRegister.cs       # Per-Vanguard warmth tracking
│   │   ├── BehavioralProfile.cs    # Pattern inference — Nemesis-inspired
│   │   └── ScholarPortrait.cs      # Seven-dimension ending architecture
│   ├── Vanguard/
│   │   ├── VanguardStateController.cs
│   │   ├── VanguardAI.cs           # Prediction-based — never mirroring
│   │   ├── VanguardDialogue.cs
│   │   └── VanguardConflictState.cs # Man in High Castle: traversal competition
│   ├── Scholar/
│   │   ├── ScholarController.cs
│   │   ├── TDSController.cs
│   │   ├── FireVessel.cs
│   │   ├── Astrolabe.cs
│   │   └── DarkVoiceResponseLog.cs # Metacognition tracking
│   ├── World/
│   │   ├── WorldManager.cs
│   │   ├── TraversalFocalPoint.cs
│   │   ├── ObeliskController.cs
│   │   └── BoundaryManager.cs
│   ├── Systems/
│   │   ├── USS/
│   │   ├── TCS/
│   │   ├── SRS/                    # Now reads ScholarPortrait + EndingTier
│   │   └── ChildPhaseDirector.cs   # Two-input: tier + portrait
│   └── Audio/
│       ├── DarkVoiceController.cs
│       └── ResonanceAudioSystem.cs
├── Scenes/
│   ├── Demo_ResonanceObelisk.unity
│   └── Prototype_BMS.unity
└── Design/
    └── kenoma_compact_context.html
```

---

## The Four Iron Laws — Never Break These

1. **Never make the turn a betrayal.** VA tells the Scholar (Clause 18) exactly what is about to happen. The turn is a completion. The warmth was genuine AND it was calculation. Both were always true.
2. **Never break the Iron Rule.** Knowledge from World B enables action in World A. Material from World A changes World B physically. One rule. Everywhere. Always.
3. **Never show the Behavioral Model.** No UI, no score counter, no "your choice has been remembered." The player reads the BMS only through Vanguard behavior changes.
4. **Never make a puzzle without an author.** Every puzzle exists because a real person made a real decision. Ask: who was here, what did they need, what did they leave?

**Iron Law V — New:** Neither world is primary. No camera system, audio mix, resource balance, or puzzle difficulty may imply that one world is the "real" world and the other is a shadow of it. The Archive of Two Truths has two truths, equally weighted.

**Iron Law VI — New:** The Vanguards are competitors, not allies. No dialogue, AI behavior, or scene staging may imply they are working toward the same goal. Their warmth toward the Scholar is real. Their competition with each other is also real. Both are always true in the same gesture.

---

## The BMS — The Most Critical System

`BMSController` is a singleton that:
- Records 12 event types batched **per room-session**
- Maintains `wa_warmth` and `vb_warmth` registers (ints, clamped −20 to +20)
- Maintains `BehavioralProfile` (pattern inference — recalculated per event)
- Tracks `wasVanguardObserved` flag per event (for Model Gap calculation)
- **NEVER exposes any of this to any UI element**
- Pushes updates to `VanguardStateController` and `VanguardAI.OnProfileUpdated`
- Reads by `SRS` at Act III alongside `ScholarPortrait` computation

### The Seven Ending Dimensions (ScholarPortrait)

The score selects the ending **tier**. The ScholarPortrait selects how the ending is **delivered**:

1. **Temporal Arc** — when the Scholar gave, not just how much (ascending / descending / erratic)
2. **Behavioral Coherence** — consistent identity vs. contradictory behavior (variance of score axes)
3. **The Model Gap** — divergence between Scholar's real engagement and what Vanguard observed
4. **Rhythm** — contemplative / efficient / restless / oscillating dwell patterns
5. **The Unread Archive** — which keystone tablets were never touched (absence as character data)
6. **Scholar Metacognition** — did the Scholar know? Did they continue anyway? (Dark Voice log)
7. **The Final Gesture** — what the Scholar was doing in their last room before Lion Phase

---

## The Vanguards — Who They Are

**Both Vanguards are in their late 20s to mid-30s.** They entered the Archive years before the Scholar — VA through the Apadana gate, VB through a crossing point deep in what became World B. The Archive's temporal mechanics have preserved them physically. Each has lived years of subjective time in their respective world. This is not a supernatural immortality: it is isolation and the Archive's unique relationship with time.

**VA (Sacred Fire):** Arrived in her early 20s as an administrative scholar sent to catalog the Archive. Found herself alone. Became military through necessity — survival in World A required managing resources, routing creature patrols, maintaining the fire altars. She is in her early 30s now. Her warmth toward the Scholar is genuine: she has not had a peer since she arrived.

**VB (The Hollow):** Arrived as a philosophical student seeking the Archive's founding texts. Found World B and could not leave. Taught herself Babylonian, read everything, wrote a 250-year-old (her subjective time) philosophical text that she knows is wrong about one thing. She is in her late 20s, possibly early 30s. Her warmth toward the Scholar is intellectual intimacy — she has been alone with ideas and no one to share them with.

**Both need the Scholar's completed model to gain traversal capability.** Neither has ever told the other this is possible. They discovered it independently from different Archive texts.

### Five Recognition Stages (both Vanguards)

- **S1** — Questions (gathering methodology data)
- **S2** — Stops asking (knows the Scholar's methods)
- **S3** — Anticipates / pre-stages
- **S4** — Answers before asked / reveals private knowledge
- **S5 ⚠** — Already knows. Observing only. **Traversal threshold approaching.**

---

## The Iron Rule (Crossing System)

- Every crossing increments `traversalDebt` on Scholar only
- Vanguard traversal debt = 0 always (they cannot cross — yet)
- Boundary: Debt 2 = 8s | Debt 3 = 20s | Debt 4+ = persistent
- **Neither world is primary. The Scholar pays the asymmetric cost because they are the bridge.**
- At Act III, whichever Vanguard completes her model first crosses for the first time.

---

## Signifier Design — Not Diegetic Purity

All status communication is evaluated by **signifier legibility** (Norman) and **immersion rupture risk** — not by a binary diegetic/non-diegetic distinction. The correct question: does this element communicate the hidden affordance before the player moves past it?

**Preattentive-reliable signals (mandatory):**
- Scholar gaze direction (peripheral motion + social gaze-following — two preattentive channels)
- Camera composition (framing the significant object)

**Preattentive-low-salience (scope-restricted):**
- Fire vessel flame lean (direction cue — habituates if overused, fire only for Archive-significant objects)

**Attentive-supplementary:**
- Astrolabe resonance (requires active listening — useless in creature-threat inattentional blindness)
- Scholar murmur (TDS VO during deep-read)

**All indicators are persistent states, not one-shot triggers.** They re-activate after camera cuts. The signal persists until the Scholar leaves the object's radius.

**Accessibility overlay layer** (settings menu, not default): high-contrast interactable highlight, subtitle track for Scholar murmurs, haptic alternatives for all audio-channel indicators. Designed simultaneously — not retrofitted.

---

## Audio Architecture

Dark Voice is binaural, not reverb. FMOD with HRTF. Spatial origins:
- **Behind** = suppressed thought surfacing against Scholar's will
- **Beside** = strategic analysis running in parallel
- **Ahead** = warning about what Scholar is about to do

**The Metacognition Log** tracks Dark Voice responses per session: Suppress / Acknowledge / Follow. The pattern "Acknowledge-then-Suppress across 3+ sessions" unlocks the Recognition Ending variant regardless of score tier.

World A: warm brass harmonics, fire altar crackle.
World B: near-silence, Scholar's fire vessel = only sound anchor.

**Neither world's audio is subordinate to the other. Both are fully designed. The asymmetry is in the Scholar's relationship to each — not in production priority.**

---

## Zero HUD — Signifier Design

| Game State | Signifier | Preattentive? |
|---|---|---|
| Oil level | Fire vessel flame VFX scale | Low-salience preattentive |
| Scholar health | Robe damage + posture degradation | Attentive |
| Creature proximity | Astrolabe vibration | Attentive (audio) |
| World identity | Lighting temperature + audio mix | Preattentive (color) |
| Traversal pressure | Boundary ambient rising | Attentive (audio) |
| Vanguard stage | Behavioral observation only | Change blindness tool |

**Change blindness is a design tool, not only a failure mode.** The Vanguard's Stage 1→2→3 evolution works precisely because players are inattentionally blind to behavioral change while task-focused. The horror of Lion Phase is retrospective: "She was always doing this and I couldn't see it." Design the blindness deliberately.

---

## Coding Conventions

- All events tagged with `const string` in `BMSEventTags.cs`
- All FMOD paths in `AudioPaths.cs`, room IDs in `RoomIDs.cs`
- Every `BMSEvent` struct carries `wasVanguardObserved: bool`
- `BehavioralProfile` recalculated on every `RecordEvent()`, never stored separately
- `ScholarPortrait` computed once at Act III trigger, passed to `ChildPhaseDirector`
- `VanguardConflictState` tracks which Vanguard is closer to traversal threshold
- No magic strings, no coroutine-based BMS dispatches, no UI reads of BMS data

---

## System Build Order

```
BMS (SYS-01) → RSS (SYS-02) → TDS (SYS-03) → TVS (SYS-04)
→ RES (SYS-05) → TCS (SYS-07) → SRS (SYS-08) → USS (SYS-06)
→ ScholarPortrait (SYS-09) → ChildPhaseDirector (SYS-10) → VanguardConflictState (SYS-11)
```

---

## Available Custom Commands

| Command | Does |
|---|---|
| `/iron-check` | Verifies file against all six Iron Laws |
| `/bms-event` | Scaffolds new BMS event with BehavioralProfile impact |
| `/new-puzzle` | Scaffolds puzzle — enforces Iron Law IV |
| `/vanguard-dialogue` | Writes Vanguard dialogue in correct voice and stage register |
| `/dark-voice` | Writes Dark Voice lines with binaural origin + metacognition tag |
| `/crossing-logic` | Generates traversal focal point crossing code |
| `/consequence-table` | Generates BMS consequence table for a solution set |
| `/scene-review` | Reviews scene against KENOMA design principles |
| `/creature-naming` | Generates Naming combat sequence |
| `/demo-check` | Runs full demo verification checklist |
| `/steal-the-flame` | Scaffolds Vessel Sacrifice puzzle variant |
| `/scholar-portrait` | Computes and describes a ScholarPortrait from run data |
| `/vanguard-conflict` | Designs a scene around the Man in High Castle competition mechanic |
| `/sprint-plan` | Generates day-by-day engineering sprint with acceptance criteria |

## Available Agents

| Agent | Invoke When |
|---|---|
| `narrative-guardian` | Before merging anything touching Vanguard behavior, puzzle design, or world balance |
| `bms-architect` | Designing or modifying BMS events, BehavioralProfile, ScholarPortrait |
| `unity-systems` | Implementing any of the 11 core systems |
| `playtester` | Simulating player experience before building |

## Document Authority

Story always beats production.
1. Storytelling Bible v8
2. Complete Narrative + Phase Design Doc
3. Game Loop & Systems
4. GDD v5

**The outer ring changes. The inner ring does not.**
