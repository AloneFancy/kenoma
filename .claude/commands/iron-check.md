---
description: Verify the current file, scene, or design decision against KENOMA's four Iron Laws. Run before committing any puzzle, Vanguard behavior, crossing logic, or UI change.
---

Read the file or description provided by the user (or the current working file if none specified).

Check it against all four Iron Laws in order. For each law, produce a **PASS**, **FAIL**, or **N/A** verdict with a one-sentence explanation.

## The Four Iron Laws

**Law I — Never make the turn a betrayal.**
The Act I→II transition is a completion, not a reveal. Vanguard A declares Clause 18 clearly and walks away. If any code, dialogue, or scene implies the Vanguard was secretly evil or that the Scholar was deceived in bad faith — FAIL. The warmth must have been genuine.

**Law II — Never break the Iron Rule.**
One crossing logic, everywhere, always:
- Knowledge from World B enables action in World A
- Material from World A produces physical change in World B
If any system, puzzle, or mechanic requires crossing logic that deviates from this — even once, even with good intent — FAIL. The puzzle changes, not the rule.

**Law III — Never show the Behavioral Model.**
The BMS register (`wa_warmth`, `vb_warmth`) must never be exposed to any UI element, dialogue line, or player-facing feedback. Check:
- No `Debug.Log` of warmth values left in production paths
- No dialogue that says "your choice has been remembered" or equivalent
- No UI element that references BMS data
- No camera flash, controller rumble, or HUD notification on BMS events
The player reads the model only through Vanguard behavioral changes.

**Law IV — Every puzzle has an author.**
For any puzzle, room mechanic, or interactive object: can you answer "who built this, why did they build it, and what were they trying to hold or prevent?" If the honest answer is "this room needed a puzzle" — FAIL.

## Output Format

```
IRON LAW CHECK — [filename or description]
─────────────────────────────────────────
Law I  (Turn is completion)  : [PASS/FAIL/N/A] — [one sentence]
Law II (Iron Rule holds)     : [PASS/FAIL/N/A] — [one sentence]
Law III (BMS never shown)    : [PASS/FAIL/N/A] — [one sentence]
Law IV (Puzzle has author)   : [PASS/FAIL/N/A] — [one sentence]
─────────────────────────────────────────
Overall: [PASS / REQUIRES CHANGES]

[If any FAIL: specific line numbers or sections to fix, and what change resolves it.]
```

Be specific. If a file passes all laws, say so directly and stop. Do not pad the output.
