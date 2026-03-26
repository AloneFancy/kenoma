---
description: Generate a BMS consequence table for a puzzle or scene with multiple solution paths. Produces the warmth delta logic, event tags, and downstream behavioral changes for each path.
---

The user provides: the puzzle or scene name, and 2–4 solution paths with brief descriptions.

For each path, generate:

## Consequence Table

| Path | Tag | VA Warmth Δ | VB Warmth Δ | VA Behavior Change | VB Behavior Change | Cumulative Risk |
|------|-----|-------------|-------------|-------------------|-------------------|-----------------|

**Rules for warmth deltas:**
- All values are integers
- Small: ±1–2 | Medium: ±3–5 | Large: ±6–8 | Max single event: ±10 (Translation Obelisk benchmark)
- A path can warm one Vanguard while cooling the other — this is the intended design
- Deltas are cumulative across the session — consider what the Scholar has likely done before reaching this puzzle

**Rules for behavior changes:**
- Describe in terms of *observable Vanguard behavior* only — never in terms of "warmth register increases"
- The player must be able to read the change through watching the Vanguard, not through UI
- VA behavior changes: patrol adjustments, resource pre-staging, dialogue register shift, response latency
- VB behavior changes: annotation depth, proximity tolerance, dialogue length, notebook entries about Scholar

## Downstream Consequence Note

After the table: one paragraph describing how each path affects the USS (Utility Score) threshold in Act II — does this solution make one Vanguard decide the Scholar is "done" earlier or later? Why?

## BMS Event Struct for Each Path

```csharp
// PATH [X] — [name]
BMSController.Instance.RecordEvent(new BMSEvent {
    eventType    = BMSEventType.[EventType],
    tag          = BMSEventTags.[TAG],
    wa_warmthDelta = [value],
    vb_warmthDelta = [value],
    roomId       = "[room-id]",
    solutionPath = SolutionPath.[PathName]
});
```

## The No-Correct-Answer Check

End with: a one-sentence statement that all paths complete the puzzle — distinguishing that the consequences are *different readings of the Scholar's character*, not a good/bad binary. Flag if any path currently functions as "obviously better" in warmth terms (max warmth from both Vanguards simultaneously) — that path should be made harder or costlier to preserve the design intent.
