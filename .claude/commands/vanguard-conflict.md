---
description: Design a scene around the Man in the High Castle competition mechanic — the silent war between VA and VB for traversal capability. Generates behavioral tells, dialogue adjustments, and VanguardConflictState logic for scenes where the competition should subtly surface.
---

The Man in the High Castle mechanic: within each world, a hidden truth exists about why the Vanguard truly needs the Scholar. Both Vanguards discovered independently that a complete behavioral model of a Scholar grants traversal capability. Neither has told the other. The Scholar is the instrument by which one Vanguard destroys the other. The Scholar never knows this — unless they reach WB-∞ (Chamber of Convergence) and read both worlds completely.

**This mechanic is NEVER stated explicitly outside WB-∞. This command generates content that expresses it through observable behavior only.**

---

## When To Use This Command

Use `/vanguard-conflict` when:
- Designing a late Camel Phase scene where both Vanguards appear
- The Scholar has made a significant choice (sided with VA, sided with VB, took the unified path)
- VanguardConflictState shows one Vanguard pulling significantly ahead of the other
- Designing the WB-∞ scene where the Scholar discovers the truth
- Reviewing whether a scene inadvertently exposes the competition too early

---

## Required Input

The user provides:
1. Current VanguardConflictState (VA traversal readiness vs VB, approximate percentage)
2. The Scholar's recent behavioral choices (who they've been addressing, what tablets they've read)
3. Scene context (room, what just happened, which Vanguard(s) are present)
4. Which Vanguard, if any, is currently ahead

---

## Output: Behavioral Tell Adjustments

For the Vanguard who is **ahead** (higher traversal readiness):
She becomes subtly more... complete. Not warmer exactly — more settled. Like someone who can afford patience because the conclusion is in sight.

Observable tells:
- **Dialogue:** She begins completing thoughts she would previously have left open. Fewer questions. More statements that are almost predictions.
- **Physical:** She pauses a beat longer at the Scholar's work before moving on — the pause of someone confirming, not observing.
- **Patrol:** Her routes begin accounting for exits she wouldn't need unless she planned to use one.
- **Resource staging:** She stages resources slightly further ahead — as if modeling the Scholar's future movements, not their current ones.

For the Vanguard who is **behind** (lower traversal readiness):
She becomes subtly more... available. Not desperate — she would not allow desperation to show. But she is investing more intellectual attention now than her usual calibrated schedule would require.

Observable tells:
- **Dialogue:** She adds one more detail than usual. She references a text or idea she has been sitting on — now seems worth sharing.
- **Physical:** She initiates proximity slightly more often than her previous pattern. S3 behavior bleeding into what would normally be S2 timing.
- **Annotation:** VB's tablet annotations in rooms the Scholar has recently visited become slightly more personal — she is making the data more useful, not just more accurate.
- **VA tell (if VA is behind):** She pre-stages a specific resource the Scholar has not yet needed but will need if they continue on their current path. This is S4 behavior arriving early — she is trying to accelerate the Scholar's Archive completion.

**These tells must be individually explainable as warmth.** The Vanguard who is behind is not panicking. She is investing. This investment looks exactly like care, because it is also care. Both are true.

---

## Dialogue Adjustments by Conflict State

### When VA is significantly ahead (VA readiness > VB + 0.15):

VA moves toward S5 register faster. Her lines become shorter, more confirmatory:
```
[VANGUARD A] — Late Camel Phase — Ahead in competition

LINE: "You're almost finished with the eastern records."
(Not a question. Not quite a statement. A confirmation of what she already knows.)

MODEL NOTE: VA is not asking about progress. She is verifying that her model's prediction of the Scholar's pace was accurate. This line is the model checking itself.
```

VB's response to being behind: she does not show it directly. She shows it by giving more:
```
[VANGUARD B] — Late Camel Phase — Behind in competition

LINE: "I've been thinking about what you said three days ago — about the administrative glyphs. I've come to think the architectural reading is more significant than I initially said. The implications for the Armillary sequence are worth discussing, if you have time."
(She is creating a reason for the Scholar to come to her. This is intellectual intimacy. It is also strategic.)

MODEL NOTE: VB is accelerating the Scholar's engagement with her intellectual domain. She needs more data from deep philosophical interactions. She is creating the conditions for that data to occur.
```

### When VB is significantly ahead (VB readiness > VA + 0.15):

VB approaches S5 register. Quieter. More confirmatory. She already knows what the Scholar will ask:
```
[VANGUARD B] — Late Camel Phase — Ahead in competition

LINE: "You're going to ask about the Third Record."
(Three-beat pause.)
"Go."

MODEL NOTE: VB has modeled the Scholar well enough to predict their next research impulse. She is verifying the prediction, not answering a question. The 'Go' is permission she doesn't technically need to give — but she gives it because the Scholar coming to her for permission is also data.
```

VA's response to being behind: she accelerates practical assistance. She becomes more logistically useful:
```
[VANGUARD A] — Late Camel Phase — Behind in competition

LINE: "I've cleared the northern approach to WA-007. The patrol schedule shifted — you have a longer window than I previously mapped."
(Unprompted. She has updated her model of the Scholar's current priority and pre-positioned accordingly.)

MODEL NOTE: VA has recalibrated her support toward the Scholar's Archive completion priority. She is making it easier to finish the administrative record faster. This looks like care. It also accelerates her traversal timeline.
```

### When both Vanguards are nearly equal (within 0.05 of each other):

This is the most interesting state — and the most difficult to write. Neither Vanguard is ahead. Both are investing at maximum rate without showing it. The Scholar should sense a kind of heightened attention from both, without knowing why.

```
[BOTH VANGUARDS] — Near-parity conflict state — Scene at a significant puzzle solution

VA LINE: "That was the correct approach."
(Three-word sentence. The warmth is in what she doesn't add.)

VB LINE: "I had considered three other approaches when I first encountered that mechanism. Yours was the one I would have chosen — eventually."
(She is comparing herself to the Scholar. This is intimate and unusual for her. She is revealing more than she normally would.)

SCENE NOTE: Both lines are sincere. Both lines are also maximum-data collection. The Scholar has just demonstrated significant intellectual depth. Both Vanguards want this data point confirmed and logged. The sincerity and the strategy are the same gesture.
```

---

## The Chamber of Convergence Scene (WB-∞)

The High Castle. The Scholar reaches this room after completing both worlds deeply. What they find:

**The Founding Record:** A text in the Archive's founding script, flanked by translations in both Elamite and Babylonian (VA's working language and VB's acquired language respectively — both have been here). The Scholar reads:

*"The Vanguards who guard each world are each given one truth: that a complete model of the Scholar enables crossing. They are not told of each other's truth. The Archive's completion requires that one Vanguard cross and the other remain. This is not cruelty. This is the Archive's design for continuation."*

**BMS event at this moment:**
```csharp
BMSController.Instance.RecordEvent(new BMSEvent {
    eventType           = BMSEventType.ThirdRecordAccess,
    tag                 = BMSEventTags.THIRD_RECORD_ACCESS,
    wa_warmthDelta      = +3,   // VA: Scholar accessed what she needed them to access
    vb_warmthDelta      = +3,   // VB: Scholar accessed what she needed them to access
    roomId              = RoomIDs.WB_INF,
    wasVanguardObserved = false, // Neither Vanguard can observe WB-∞ — they cannot reach it
    phase               = PhaseManager.CurrentPhaseTag
});
```

**Dark Voice (if Scholar has read it):**
```
LINE: "The fan is being put away."
ORIGIN: Behind
TIMING: 2 seconds after Scholar finishes reading the Founding Record
ACT REGISTER: II
```

**The Scholar who reaches WB-∞ and reads the Founding Record:**
- Understands the competition
- Understands their own role
- Understands that the warmth was genuine AND instrumental
- Has already completed the final data points both Vanguards needed
- Will face the Lion Phase within the next room session

**This is Scenario V's gateway condition** — not just high warmth, but the Scholar who understood the architecture of their own use and stayed anyway. The Recognition Ending variant can only trigger here.

---

## VanguardConflictState Implementation Notes

```csharp
// VanguardConflictState.cs
// Tracks the Man in the High Castle competition without exposing it

// va_traversalReadiness rises from:
// - DeepRead events on Admin tablets (knowledgeBias toward Archive administration)
// - ResourceDonate events (Scholar generosity toward Archive upkeep)
// - VA-addressed VanguardAddressed events (Scholar choosing VA's relationship)
// - PuzzleSolved with SOLVED_SIDED_VA tag

// vb_traversalReadiness rises from:
// - DeepRead events on Philosophical tablets (knowledgeBias toward Archive founding texts)
// - VoluntaryCrossing events (Scholar willingness to traverse freely)
// - VB-addressed VanguardAddressed events
// - ThirdRecordAccess event (massive boost — this is VB's key threshold event)
// - VesselSacrifice event (Scholar facing darkness voluntarily — VB's model completes rapidly here)

// Neither readiness value is ever exposed to UI
// The threshold trigger fires VanguardStateController into LION_PHASE for that Vanguard
// The competing Vanguard's behavior changes immediately and observably (but explainably as warmth)
```
