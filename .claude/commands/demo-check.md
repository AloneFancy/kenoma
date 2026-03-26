---
description: Run the full demo verification checklist. This is the single gate before the demo build is considered externally showable. One verdict only.
---

Review the current demo scene (Demo_ResonanceObelisk or specified scene) against all demo requirements.

## The Only Verdict That Matters

**"The Vanguard treated me differently based on what I chose."**

If a playtester can say this without being prompted — the demo works.
If a playtester describes only their own actions ("I chose to help one side") and not the Vanguard's response — the BMS is running but not surfacing through behavior. That is a failure state.

---

## Section 1: Core Mechanic Proof

- [ ] Three solution paths are all completable (none produces a broken state or softlock)
- [ ] No solution path is marked or hinted as "correct" anywhere in the experience
- [ ] All paths produce a different BMS record (verify in BMSController event log)
- [ ] Vanguard A's behavior is observably different after Path A vs Path B vs Path C
- [ ] Vanguard B's behavior is observably different after Path A vs Path B vs Path C
- [ ] The behavioral difference is readable without any UI explanation

## Section 2: Traversal Verification

- [ ] Crossing 1: Scholar enters WB — Traversal Debt = 1, Boundary does not appear
- [ ] Crossing 2: Scholar returns to WA — Traversal Debt = 2, Boundary manifests for 8 seconds then retreats
- [ ] Crossing 3: Scholar crosses again — Traversal Debt = 3, Boundary pursues for 20 seconds
- [ ] Vanguard traversal debt remains 0 throughout (verify WorldManager)
- [ ] Iron Rule: Scholar cannot solve WA Obelisk without knowledge gained in WB

## Section 3: Zero HUD Verification

Run the demo with a fresh player who has not been briefed. They must be able to determine the following **without UI**:

- [ ] Approximate oil level (fire vessel flame size)
- [ ] Whether a creature is nearby (astrolabe vibration)
- [ ] Whether the Scholar is in World A or World B (lighting, temperature of audio, architecture)
- [ ] Whether a Vanguard is present in the room (behavioral cues before visual confirmation)

## Section 4: Audio Verification

- [ ] Dark Voice lines play with correct spatial origin (test with headphones — should feel behind/beside/ahead, not as reverb echo)
- [ ] World A ambient: warm brass present, fire altar crackling
- [ ] World B ambient: near-silence — Scholar's fire vessel is the only warm audio anchor
- [ ] Lantern-Thief crystalline approach tone is present and escalating
- [ ] Vanguard A's tools produce distinct stone-on-stone sounds
- [ ] Vanguard B's writing implements produce soft, deliberate sounds

## Section 5: Iron Law Compliance

Run `/iron-check` on:
- [ ] `ObeliskController.cs`
- [ ] `TraversalFocalPoint.cs`
- [ ] `VAStateController.cs`
- [ ] `VBStateController.cs`
- [ ] `BMSController.cs`

All must pass all four laws.

## Section 6: Demo-Specific Consequence Card

- [ ] Card appears after Scholar reaches fire altar post-puzzle (outside gameplay — demo context only)
- [ ] Card shows Vanguard assessments in Vanguard voice (not in game-system language)
- [ ] Card shows no numerical scores
- [ ] Card shows no good/bad framing
- [ ] Card displays for 8 seconds or until player input

## Section 7: Path C Gate

- [ ] Path C (unified) is only available if Scholar completed WA deep-read AND read VB's notation tablet
- [ ] Scholar who skipped either of these cannot access Path C and is not told why
- [ ] Verify: `canAccessPathC = (tds.waFriezeRead && tds.vbNotebookRead)` evaluates correctly

---

## Output

```
DEMO VERIFICATION — [build date]
────────────────────────────────────────────────
Core Mechanic    : [PASS/FAIL] — [playtest evidence or gap]
Traversal        : [PASS/FAIL]
Zero HUD         : [PASS/FAIL]
Audio            : [PASS/FAIL]
Iron Laws        : [PASS/FAIL] — [which files, which laws]
Consequence Card : [PASS/FAIL]
Path C Gate      : [PASS/FAIL]
────────────────────────────────────────────────
DEMO STATUS: [EXTERNALLY SHOWABLE / NOT YET]

[If not showable: the single most critical blocking issue only.
Fix that. Run again. One thing at a time.]
```
