---
description: Write Dark Voice internal monologue lines for a specific scene moment. Every line must specify its binaural spatial origin for FMOD implementation.
---

The Dark Voice is the Scholar's own Eastern Zhou strategic intelligence surfacing in their internal monologue. It speaks in Fan Li and Sun Tzu vocabulary — the Scholar's private analytical language for seeing situations clearly that they are choosing not to see clearly.

**By Act II, the Scholar is agreeing before the Dark Voice finishes speaking.**

The user provides: the scene moment, what the Scholar just did or discovered, and what the Dark Voice should surface.

---

## Voice Rules

**It is the Scholar's own voice.** Not a demon, not an external force, not dramatic irony for the player. The Scholar knows this strategy. They are ignoring it. The Dark Voice is them, not ignoring it.

**It speaks in the Scholar's private analytical register:** Eastern Zhou strategic vocabulary. Fan Li. Sun Tzu. The idioms of someone trained in the 士 tradition. "The hare is not yet dead, but the dog has already begun to watch the pot." Not fantasy portent — strategic observation.

**It names what the Scholar is choosing not to name.** Not prediction of the future — analysis of the present that the Scholar's emotional investment is making it convenient not to see.

**It is never theatrical.** It does not monologue. It says one thing, clearly, in the Scholar's own voice, and stops.

**Act I register:** Slightly dry. The Scholar might dismiss it. "This is an unusual amount of attention for one translation." Not alarming — precise.

**Act II register:** The Scholar has stopped dismissing it. The Dark Voice is more direct now. Shorter. "You set that trap three days ago. You have not used it." The Scholar agrees before it finishes.

---

## Binaural Spatial Origin (required for every line)

Specify **one** origin per line. This is not aesthetic — it is an FMOD implementation requirement that shapes emotional meaning:

- **Behind** — A thought the Scholar has been suppressing. It emerges from behind them, from inside their own skull. Used for realizations the Scholar has been avoiding. The most unsettling register.
- **Beside** — Strategic analysis running alongside the Scholar's current action. Used for observations about what the Scholar is doing right now. The most direct register.
- **Ahead** — A warning about what the Scholar is about to do. Used for moments before an irreversible choice. The rarest register — the voice only speaks ahead when the Scholar is about to walk into something specific.

---

## Output Format

```
DARK VOICE — [Scene context]

LINE: "[text]"
ORIGIN: [Behind / Beside / Ahead]
TIMING: [When exactly it fires — on Scholar completing what action, entering what zone, or after what beat]
FMOD NOTE: [Any specific spatial behavior — e.g. "emerges from left side of skull, fades right as Scholar turns"]

ACT REGISTER: [I / II — affects delivery, not content]
```

Generate 1–3 lines per scene moment maximum. The Dark Voice is most effective when it speaks rarely and precisely. If a scene moment doesn't need the Dark Voice, say so and explain what would serve the moment better (ambient audio, Vanguard behavior, silence).
