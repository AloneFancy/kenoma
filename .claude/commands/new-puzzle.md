---
description: Scaffold a new KENOMA puzzle. Enforces Iron Law IV — every puzzle must have an author. Will refuse to generate puzzle mechanics until the authorship question is answered.
---

Before generating any puzzle code or design, ask the user three questions. Do not proceed until all three are answered:

1. **Who built this mechanism?** (A specific person or role within the Archive's original civilization — e.g. "the chief astronomer responsible for synchronizing the crossing points", "a junior archivist who feared the Lantern-Thieves and built a light-diffusion trap")

2. **What did they need it to do?** (The original practical purpose — not "it's a puzzle for the player" but the in-world function the mechanism served)

3. **What went wrong, or what secret does it hold?** (Why is it in its current state? What does the Scholar discover about this person through solving it?)

If the user cannot answer these questions, prompt them to answer before continuing. The mechanism exists in the Archive because a person put it there. That person is the puzzle's design authority.

---

Once answered, generate:

## 1. Puzzle Header (for design doc)

```
PUZZLE ID: PZ-[ZONE]-[###]
ROOM: [WA-/WB-ID]
AUTHOR: [Name or role of the person who built this mechanism]
ORIGINAL PURPOSE: [What it was designed to do]
CURRENT STATE: [What the Scholar finds 300 years later]
IRON RULE USAGE: [How World A ↔ World B information exchange applies]
```

## 2. Solution States

List 2–3 solution paths. For each:
- What the Scholar must do (actions, world crossings required)
- What they need to know first (prior translations, items, Vanguard interactions)
- BMS consequence (which Vanguard's warmth register changes, by how much, why)

**Remind the user: no solution is correct. Solutions that pass are all valid. Their cost is different.**

## 3. C# Scaffold

Generate a `PuzzleController` MonoBehaviour for this specific puzzle:
- Inherits from `BasePuzzleController` 
- `[PuzzleID]` attribute set
- `OnSolutionAttempt(SolutionPath path)` method routing to each outcome
- `BMSController.Instance.RecordEvent()` call for each solution path
- `OnDeepReadComplete()` hook (for if the Scholar reads the authorial inscription — extra warmth)
- **No yield-based coroutines for BMS events** — dispatch immediately on completion

## 4. Audio Notes

Specify: what sound does the mechanism make when in its broken state? What sound plays on each solution? Does the Scholar's Dark Voice comment — and if so, from which spatial origin (behind / beside / ahead)?

## 5. Author's Inscription

Write 2–3 lines of in-world text (in translated form) that the Scholar can find in the room — the author's own words explaining what they built and why. This is the deep-read content. It should make the puzzle's solution feel like understanding a person, not cracking a code.
