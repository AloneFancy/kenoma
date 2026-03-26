---
description: Generate a focused engineering sprint plan for a specific KENOMA system or feature. Respects system build order. Produces day-by-day tasks with acceptance criteria.
---

The user provides: the system or feature to sprint on, the team size, and the sprint length (default 2 weeks / 10 working days).

## Before Planning — Build Order Check

State which systems are prerequisites for the requested sprint. If any prerequisite is not yet stable, flag it and recommend sprinting on the prerequisite first. The build order is:

```
BMS → RSS → TDS → TVS → RES → TCS → SRS → USS
```

Never plan a USS sprint if RSS, TDS, or TVS are not marked stable.

## Sprint Plan Structure

### Sprint Goal (one sentence)
What observable capability exists at the end of this sprint that did not exist at the start.

### Acceptance Criteria (the only things that determine done)
3–5 criteria. Each one must be falsifiable — either it passes or it fails. No subjective criteria.

For any system sprint, always include:
- `[ ]` The system runs without error in Demo_ResonanceObelisk.unity
- `[ ]` `/iron-check` passes on all new files
- `[ ]` No BMS warmth data surfaces to any UI element
- `[ ]` All BMS event tags are constants from BMSEventTags.cs

### Day-by-Day Tasks

Format each day:

```
Day [N] — [Focus area]
Task: [Specific deliverable]
Files: [Which files to create or modify]
Test: [How to verify it worked — one specific check]
Blocked by: [Any dependency that must be resolved first, or "nothing"]
```

### Risk Flags

List any risks specific to this sprint — not general risks, specific ones for this system at this moment in the project. Reference the 12 risk flags from the Game Loop & Systems document where relevant.

### Integration Points

Which other systems does this sprint touch? What events does it fire or consume? What is the contract between this sprint's output and the next system in the build order?

### Definition of Ready to Merge

One sentence: what state must the system be in before merging to `dev`. This must include `/scene-review` passing on the demo scene.
