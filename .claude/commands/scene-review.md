---
description: Review a Unity scene setup against KENOMA's design principles. Checks camera composition, audio diegetics, BMS wiring, Vanguard AI states, and Iron Laws. Run before any scene is considered feature-complete.
---

Read the scene description, hierarchy dump, or script files provided. Then run through the following checklist in order. Report PASS, FAIL, or NEEDS REVIEW for each.

---

## Camera Checklist

- [ ] Fixed cameras only — no free camera, no follow camera
- [ ] Every camera position frames: Scholar position + Vanguard position + key interactive object simultaneously where possible
- [ ] Scholar near TFP: the other world is visible (distorted) through the ring in the camera frame
- [ ] No camera angle that obscures the Scholar's fire vessel flame (primary status indicator)
- [ ] The Vanguard's hands/tools are visible in at least one camera per room (her behavioral cues must be readable)

## Audio Checklist

- [ ] Dark Voice configured as FMOD binaural source — not a reverb send on the Scholar's VO
- [ ] Each Dark Voice line has a specified spatial origin attribute (Behind / Beside / Ahead)
- [ ] World A ambient: warm brass resonance, fire altar crackle present
- [ ] World B ambient: near-silence — Scholar's fire vessel is the only warm audio anchor
- [ ] Obelisk/mechanism audio: diegetic only — no non-diegetic music cues for puzzle feedback
- [ ] Vanguard's physical sounds (tools, footsteps, writing) are present and distinct per Vanguard

## BMS Wiring Checklist

- [ ] BMSController.Instance.RecordEvent() is called for every observable Scholar behavior in this scene
- [ ] No BMS event is dispatched on Update() — only on completed actions
- [ ] No Debug.Log of warmth register values remains in any production code path
- [ ] No UI element references BMS data
- [ ] Warmth register changes produce observable Vanguard behavior differences (test: can a playtester describe the Vanguard changed without being told?)

## Vanguard AI Checklist

- [ ] Both Vanguards have their state machine wired: correct states for this scene, correct transitions
- [ ] Neither Vanguard's traversal debt is > 0 (they never cross — verify in WorldManager)
- [ ] Vanguard A's behavior follows her military/efficiency model (not emotional)
- [ ] Vanguard B's behavior follows her philosophical/depth model (not cold — present)
- [ ] Stage 5 behavior (if scene is late Camel Phase): Vanguard speaks less, observes more — coded, not just noted in design

## Iron Law Checklist

Run `/iron-check` on the scene's primary puzzle script and primary Vanguard interaction script. Report results here.

## Traversal Checklist (if scene contains a TFP)

- [ ] Debt increments on every crossing including back-crossings
- [ ] Boundary manifests at correct debt thresholds (2 = 8s, 3 = 20s, 4+ = persistent)
- [ ] Scholar's fire vessel dims on WB entry
- [ ] 2.2-second non-interruptable transition is enforced
- [ ] "Look before you commit" peek view is implemented

---

## Output Format

```
SCENE REVIEW — [scene name]
────────────────────────────────────────────
Camera       : [PASS/FAIL/PARTIAL] — [issues if any]
Audio        : [PASS/FAIL/PARTIAL] — [issues if any]
BMS Wiring   : [PASS/FAIL/PARTIAL] — [issues if any]
Vanguard AI  : [PASS/FAIL/PARTIAL] — [issues if any]
Iron Laws    : [PASS/FAIL/PARTIAL] — [see /iron-check output]
Traversal    : [PASS/FAIL/PARTIAL/N/A]
────────────────────────────────────────────
Scene Status : [FEATURE-COMPLETE / NEEDS WORK / BLOCKED]

[Prioritized list of required changes if not feature-complete — most critical first.]
```
