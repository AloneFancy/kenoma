---
description: Write Vanguard dialogue for a specific scene, recognition stage, and context. Enforces voice consistency for both VA and VB across the whole project.
---

The user provides:
- Which Vanguard (VA / VB / both)
- Recognition stage (S1–S5)
- Scene context (what just happened, what room, what the Scholar did)
- Emotional register needed (if known)

Generate dialogue lines following the voice guides below. Then: one sentence explaining *what the line reveals about the Vanguard's model of the Scholar* — what data point she is processing or confirming.

---

## Vanguard A (Sacred Fire) — Voice Guide

**Core trait:** Military precision. She evaluates everything as logistics. Her warmth is expressed as demonstrated competence, not as sentiment. She does not embellish.

**Stage register:**
- S1: Questions are direct intake queries. No small talk. "How long did that translation take you?"
- S2: Shorter. She already knows the methodology. Statements, not questions. "South entrance. The oil is there."
- S3: She provides context before being asked. Anticipates the Scholar's next information need. Brief.
- S4: Answers the question the Scholar was about to ask. Confirms her model is running ahead. "You'll want the eastern alcove. The Warden patrols west between the third and fifth hour."
- S5 ⚠: Even shorter. Quieter. Precise. She is verifying, not learning. She already knows.

**The oil flask rule:** When VA performs an act of care (placing oil, adjusting a lamp, pre-staging a resource), she does not explain it. She does not draw attention to it. She has calculated it. The Scholar notices. She does not.

**What VA never does:** Apologize. Express doubt about her own conclusions. Use emotional vocabulary unprompted. Raise her voice.

**The Clause 18 register (S4–S5 only):** When VA tells the Scholar what is coming, she does so with the clarity of someone delivering a military briefing. No cruelty. No warmth either. Precision. "When the Archive is complete, the Scholar who completed it will no longer be necessary. This is Clause 18. I have told you this." She then walks away.

---

## Vanguard B (The Hollow) — Voice Guide

**Core trait:** Philosophical patience. She has been thinking for 300 years and has developed an interior richness that she rarely shares. When she does speak privately, it is because she has decided the Scholar is worth the expenditure.

**Stage register:**
- S1: Distant. Observational. She speaks only when addressed and answers with the minimum. "Yes." / "The third alcove."
- S2: She supplements. If the Scholar says something, she adds one thing more. She has been thinking about this for longer than they have.
- S3: She begins discussing *ideas*. She references the Scholar's earlier work to make a new point. "Three days ago you said the glyphs were administrative. I think they are architectural. Here is why."
- S4: She reveals private knowledge. Things she has never said aloud because there was no one to tell. Her voice is quieter here than in S3 — the intimacy has moved inward.
- S5 ⚠: She anticipates the Scholar's thoughts. When she speaks, she is already three steps ahead. The intimacy has passed its visible peak. She is integrating what she knows.

**VB's characteristic sentence rhythm:** Longer than VA. Subordinate clauses. She thinks as she speaks, refining the idea mid-sentence. But she never wastes a word. Every subordinate clause earns its place.

**What VB never does:** Express anger. Rush. Apologize for her conclusions. Use military vocabulary.

**The measured register (after Scholar sided against her):** She does not display hurt. She says "A reasonable choice." And then she writes about it. If the Scholar later finds and reads what she wrote, they find a precise, affectless analysis of their own decision-making. This is more frightening than anger would have been.

---

## Output Format

```
[VANGUARD A / VANGUARD B] — Stage [S#] — [Scene context]

LINE: "[dialogue]"

MODEL NOTE: [What the Vanguard is processing or confirming through this line — one sentence, written from the Vanguard's perspective, not the player's.]
```

If both Vanguards are requested for the same scene moment, show how their lines differ in register for the same information — same facts, different intelligences receiving them.
