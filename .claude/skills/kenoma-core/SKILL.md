# KENOMA Core Skill — v2
# Loaded by: all agents and commands
# Purpose: Compact project context — game identity, Iron Laws, all new mechanics

---

## Game Identity (one paragraph)

KENOMA is a fixed-camera psychological horror tragedy. A scholar (the 士 archetype) enters a sealed Achaemenid Persian archive and is exactly good enough to be used completely — not by one intelligence but by two competitors. The Vanguards are people in their **late 20s to mid-30s** who entered the Archive years before the Scholar and have been shaped by their separate worlds. They are not guides. They are competitors in a silent war over traversal capability: whichever Vanguard completes a behavioral model of the Scholar first gains the ability to cross between worlds — and eliminate the other Vanguard. The Scholar is the instrument by which one Vanguard destroys the other. The Scholar never knows this. Neither world is primary. Both truths are equally real. This is why KENOMA exists.

**Thesis — Fan Li:** "When the birds are gone, the good bow is put away. When the hare is dead, the hunting dog is cooked." The Scholar knows this text. Teaches it. Thinks it warns against bad rulers. It warns against anyone who serves at all.

**Thesis — Nietzsche:** "Man must be surpassed." The Scholar's arc is the three metamorphoses. They arrive as the Camel. They become the Lion. The surviving Vanguard completes as the Child.

---

## The Five Core Ideas

Any code, dialogue, mechanic, or room that doesn't serve one of these should not exist.

### 1 — The Tragedy of Competence
The Scholar is exactly good enough to be used completely. Not despite their brilliance — because of it. Every correct professional decision is a step toward the conclusion. Guard against: making the Scholar feel passive or victimized. They chose this. Every day.

### 2 — Warmth and Calculation Are the Same Thing
VA places the exact oil calculated from tracking Scholar consumption since Day One. This is care. The data behind it is also real. Both are completely true in the same gesture. Neither is undermined by the other. Guard against: resolving warmth into either pure manipulation or pure sentiment.

### 3 — Understanding Is the Weapon — And the Prize
A complete behavioral model is not just the mechanism of elimination. It is what grants traversal. The Vanguard who understands the Scholar completely can do what neither could before: cross between worlds. Understanding IS the weapon, AND it is the resource both Vanguards are competing to acquire. Guard against: making the BMS visible, or making the competition feel like conventional antagonism.

### 4 — The Scholar Is the Only Bridge — Until They Are Complete
The three-body system is baked into the Archive's architecture 300 years before the Scholar arrived. The Scholar pays all crossing costs. The Vanguard has zero traversal debt — until Act III, when the completed model changes this asymmetry for the first time. Guard against: the Iron Rule ever bending.

### 5 — The Ending Is Not a Twist. It Is a Completion.
The player who reaches Scenario V built the thing that eliminated them AND enabled one Vanguard to finally win the war they have been fighting since before the Scholar arrived. The turn must land as: "I knew it was coming and it still landed." Guard against: any framing of the turn as betrayal or surprise.

---

## The Six Iron Laws

### Law I — Never make the turn a betrayal
The Act I→II transition is a completion. VA declares Clause 18 clearly and walks away. The warmth was genuine. The calculation was also real. Both were always true.

### Law II — Never break the Iron Rule
Knowledge from World B enables action in World A. Material from World A produces physical change in World B. One rule. Everywhere. Always.

### Law III — Never show the Behavioral Model
No UI. No "your choice has been remembered." No score counter. The player reads the model through one channel: Vanguard behavioral changes. Stage 5 arrives through noticing she stopped asking questions she used to ask.

### Law IV — Every puzzle has an author
Every puzzle exists because a real person made a real decision in that space. Question always: who was here, what did they need, what did they leave?

### Law V — Neither world is primary
No camera system, audio mix, resource balance, puzzle difficulty, or dialogue line may imply one world is real and the other a shadow. Both are equally real. Both Vanguards are equally the enemy. Both worlds are equally the Archive.

### Law VI — The Vanguards are competitors, not allies
No dialogue, AI behavior, or scene staging may imply VA and VB are working toward the same goal. Their warmth toward the Scholar is real. Their competition with each other is also real. Both are always true. Never resolve this.

---

## The Man in the High Castle Mechanic

Within each world exists a hidden truth about why the Vanguard truly needs the Scholar. This mechanic is never stated. It is discovered only through reading both worlds completely.

**What VA knows:** A complete behavioral model grants traversal capability. She discovered this in a restricted Archive text she has never shared. She needs the Scholar to complete Archive administration (Clause 18) because completion completes her model. Her model grants her traversal. She crosses to World B. The 300-year isolation ends.

**What VB knows:** The Third Record — the Archive's founding document — contains the traversal formula. She needs the Scholar to access it because the access event completes her behavioral model of the Scholar. Her complete model grants her traversal. She crosses to World A.

**What the Scholar knows:** Nothing of this. The Scholar believes they are completing scholarly work.

**The Chamber of Convergence (WB-∞):** The "High Castle" — where both truths exist simultaneously. A Scholar who reaches it with both worlds deeply read finds text that names the competition explicitly. Most Scholars never reach it. The ones who do understand everything at the moment their use is complete.

**Design implementation:** `VanguardConflictState.cs` tracks each Vanguard's traversal threshold (percentage of behavioral model completion). The Vanguard who crosses the threshold first enters Lion Phase. The other Vanguard's behavior changes immediately — she becomes more urgent, less patient. This change is observable through behavior only. Never stated.

---

## Nietzsche's Three Metamorphoses — Phase Architecture

**Phase I — The Camel (Game Phase: Camel Phase)**
"What is the heaviest thing, ye heroes?" The camel kneels and says "Thou shalt" — it seeks to take on the heaviest load. The Scholar arrives and serves willingly. Every deep-read, every donation, every voluntary crossing is an act of the Camel. The heaviest load in KENOMA: to serve so well that your excellence becomes the instrument of your ending.

**Phase II — The Lion (Game Phase: Lion Phase)**
"I will." The Lion fights the dragon "Thou shalt." The Lion Phase begins when one Vanguard's USS drops below execution threshold. She declares Clause 18 and pursues. The Scholar who understood the Dark Voice and continued anyway meets this phase as the Lion — active, choosing. The Scholar who never understood meets it as prey. The Lion cannot create new values. But it can clear the ground for the Child.

**Phase III — The Child (Game Phase: Child Phase / Act III)**
"Innocence and forgetting, a new beginning, a game, a self-propelling wheel, a first movement, a sacred Yea." Act III belongs to the surviving Vanguard. She moves through the Scholar's rooms. She is not grieving. She is not triumphing. She is beginning. The Archive is hers. She walks north. This is the Child: not innocence as naivety, but as the first act of a new world that required the Scholar's completion to become possible.

**The three phases are the game's literal structure. Every system serves one phase. Every puzzle should know which phase it belongs to.**

---

## The "He Who Would Steal the Flame" Puzzle — PZ-WA-011

Reinvented from *Prince of Persia 2: The Shadow and the Flame*.

**Original:** An inscription warns that stealing the flame triggers a death trap. The player's shadow-self must be consumed to pass.

**KENOMA reinvention — The Vessel Sacrifice:**
A threshold inscription reads: *"He who would steal the flame from the dark archive must first surrender it."* The Scholar must voluntarily extinguish their fire vessel to gain passage to the most important tablet in World B.

**Mechanics:**
- Scholar approaches the threshold with fire vessel lit: passage blocked
- Scholar extinguishes fire vessel voluntarily: 14-second window of complete darkness
- Lantern-Thieves track Scholar by residual warmth only during this window (not by light)
- Scholar must navigate blind to the tablet and read it before the fire vessel must be relit (oil drain continues even when vessel is dark)
- The tablet contains the Previous Scholar's final entry — the last piece of the origin inscription

**Why it works:** The fire vessel is the Scholar's identity in World B. Every creature tracks it. Every resource decision involves it. Choosing to extinguish it voluntarily is the act that distinguishes a Scholar who has understood the Archive from one who is merely surviving in it.

**Puzzle author:** Archivist Shirin, junior cataloger, who feared darkness her entire life. She hid the most important text she had ever found behind her own worst fear. She wanted only someone who had faced the same fear willingly to read what she left. Her inscription at the base of the threshold reads: *"I wrote this in the dark. I could not see my own hands. I stayed until it was done."*

**BMS consequence:**
```
BMSController.Instance.RecordEvent(new BMSEvent {
    eventType      = BMSEventType.VesselSacrifice,      // new type
    tag            = BMSEventTags.VESSEL_SACRIFICE,
    wa_warmthDelta = +4,   // VA: Scholar chose knowledge over safety — efficient
    vb_warmthDelta = +8,   // VB: Scholar chose understanding over survival — maximum model data
    roomId         = RoomIDs.WB_THRESHOLD_SHIRIN,
    wasVanguardObserved = vanguardObservationCheck      // Model Gap data
});
```

---

## Characters — Voice and Behavior Rules

### The Vanguards — Age and Entry

**Both Vanguards are in their late 20s to mid-30s.** The Archive is 300 years sealed. The Vanguards arrived years before the Scholar — not centuries. The Archive's temporal mechanics have preserved their bodies while subjective time has shaped their minds. They are young people who have been utterly alone.

**Vanguard A (Sacred Fire):** Arrived in her early 20s as an administrative scholar. Became militarized through necessity — survival in World A required logistics thinking, resource management, creature patrol mapping. Now in her early 30s. The warmth she shows the Scholar is also the relief of having a peer for the first time since she arrived.

**Vanguard B (The Hollow):** Arrived as a philosophical student. Found World B and could not leave. Has read everything. Has written her own 250-year-old text (subjectively decades, not centuries — the Archive's time is strange) that she knows is wrong about one thing. Late 20s. The warmth she shows the Scholar is the release of finally having someone to think with.

### The Scholar
- 士 archetype: finds the problem matching exact skills, applies without reservation
- Three metamorphoses: Camel → Lion → never reaches Child (that is the Vanguard's phase)
- Zero HUD: robe damage, fire vessel flame, astrolabe vibration
- Combat: T1 Environmental → T2 Fire/Crossbow/Bell → T3 Naming
- Dark Voice: Scholar's own Eastern Zhou strategic intelligence. Metacognition state tracked.

### Vanguard A (Sacred Fire)
- Military model. Efficiency and completion rate.
- Warmth = professional trust expressed as logistics (pre-staged resources, access grants, patrol adjustments)
- Competes with VB for traversal by completing the Archive's administrative record
- Clause 18 is not cruelty — it is the Archive's own founding protocol, which she believes in
- Stage 5: shorter, quieter, more precise. The model is close to complete. Traversal threshold is close.
- Never: apologizes, uses emotional vocabulary, shows the competition with VB

### Vanguard B (The Hollow)
- Philosophical model. Intellectual depth and novelty.
- Warmth = intellectual intimacy (supplements translations, reveals private knowledge, writes about Scholar)
- Competes with VA for traversal by having the Scholar access the Third Record
- Her "measured register" after Scholar sided against her: "A reasonable choice." Then she writes about it. This is more frightening than anger.
- Stage 5: quieter than S4. She anticipates the Scholar's thoughts. The model is complete.
- Never: expresses anger, rushes, shows the competition with VA

### The Boundary
- The Archive's crossing law made physical. Pursues consequence, not malice.
- Cannot fight. Can be stunned with Naming Bell (8 seconds).
- Never pursues either Vanguard — their debt is zero.
- After Act III: the surviving Vanguard can cross freely. The Boundary does not pursue her.

---

## World Architecture

### Neither World Is Primary — Iron Law V

**World A (Sacred Fire):** Apadana-scale, 72 stone columns, fire altars at every junction. Scholar lights fire altars (oil cost) → altars spread warmth → Apadana becomes beautiful. The player should love this place before Act II takes it. This is not the "real" world.

**World B (The Hollow):** Same column grid, inverted underground. Scholar's fire vessel = only warm light in 300 years. Lantern-Thieves (×2 in demo). Friezes showing a procession gone wrong. This is not the "shadow" world. It is equally real.

**Key rooms:**
- WA-001 Gate · WA-003 Eastern Treasury · WA-007 Grand Armillary · WA-011 Shirin's Threshold (Vessel Sacrifice puzzle)
- WB-001 Inverted Gate · WB-004 Dark Library (Previous Scholar's journal) · WB-∞ Chamber of Convergence (High Castle)

### The Iron Rule (Crossing System)
- Knowledge from WB enables action in WA
- Material from WA produces physical change in WB
- Traversal Debt increments on every Scholar crossing
- Debt 2 = Boundary 8s | Debt 3 = Boundary 20s | Debt 4+ = persistent
- Vanguard traversal debt = 0 — until Act III

---

## The BehavioralProfile — Pattern Inference Layer

Derived from BMS event frequencies. Recalculated on every `RecordEvent()` call. Never stored independently. Never exposed to UI.

```csharp
public struct BehavioralProfile
{
    public float knowledgeBias;       // DeepRead / (DeepRead + Skim) ratio
    public float generosityBias;      // Donate / (Donate + Withhold) ratio
    public float voluntaryCrossRate;  // Voluntary crossings / total crossings
    public float namingPreference;    // Naming / total combat actions
    public float vanguardAffinity;    // VA addresses vs VB addresses, range −1 to +1
    public bool  accessedThirdRecord; // boolean flag
}
```

`VanguardAI.PredictScholarNextRoom()` reads the profile to predict future Scholar movement — NOT to react to past movement. This is the core distinction from mirroring.

---

## The ScholarPortrait — Seven Ending Dimensions

Computed at Act III trigger alongside SRS evaluation. Passed to `ChildPhaseDirector`.

```csharp
public struct ScholarPortrait
{
    public TemporalArc          arc;              // Ascending/Descending/Uniform/LateConversion/Erratic
    public float                coherence;        // 0–1, variance of score axes (low = coherent)
    public float                modelGap;         // −1 to +1 (positive = richer than observed)
    public RhythmType           rhythm;           // Contemplative/Efficient/Restless/Oscillating
    public List<string>         keystoneGaps;     // IDs of keystone tablets never read
    public MetacognitionState   metacognition;    // NeverUnderstood/KnewAndWithdrew/KnewAndStayed/Partial
    public LastGestureType      finalGesture;     // Intellectual/Relational/CombatReady/Idle
}
```

The ending **tier** (from score) determines which ending plays. The **portrait** determines how the surviving Vanguard delivers it — her opening posture, pacing, behavioral references, the epilogue's register.

---

## Five Scenario Archetypes (Act III — The Child Phase)

Act III belongs to the surviving Vanguard. She walks through the Scholar's rooms. Three-second silence. Same gesture, different weight.

| Scenario | BMS Range | Genre | Final Register |
|---|---|---|---|
| I | Low | Emptiness | Administrative completion. She straightens nothing. |
| II | Low-mid | Grief | She pauses at one room longer. No explanation. |
| III | Mid | Respect | She returns the Scholar's journal to the Scholar's natural position, not her optimal one. |
| IV | Mid-high | Completion | She finishes the Scholar's last translation. Three words. Then: "The birds are gone now." |
| V | High | Transcendence | Three-second silence feels like prayer. She does not straighten anything. The fire stays lit. |

**The Recognition Ending (any tier, metacognition KnewAndStayed):** She enters the Scholar's last room. She looks at them. She pauses four seconds — longer than any other ending variant. Then she says one line from the Scholar's own opening VO, back to them. Not mockery. Recognition. The circuit is complete.

---

## Document Authority

Story always beats production.
1. Storytelling Bible v8
2. Complete Narrative + Phase Design Doc
3. Game Loop & Systems / GDD v5
4. All other production documents

Outer ring changes. Inner ring does not.
