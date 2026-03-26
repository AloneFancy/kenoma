---
description: Generate the content of an Archive tablet — the text the Scholar translates during a deep-read. Tablets must be authored documents from real people in the Archive's history, not generic lore drops.
---

The user provides: room ID, tablet purpose (what the Scholar needs from it), and any known BMS consequence if the Scholar deep-reads vs skims.

## Tablet Authorship Requirements

Every tablet was written by a real person at a real moment. Before writing the tablet content, answer:
- **Who wrote this?** (role, circumstances, when in the Archive's history)
- **Why did they write it?** (administrative record, personal note, emergency protocol, philosophical argument, grief, warning)
- **What did they not know when they wrote it?** (what the reader 300 years later knows that the author didn't)

The gap between what the author knew and what the Scholar knows is where the tablet gets its power.

## Tablet Content Structure

**Translation header (in italics):** The Scholar's internal annotation of the document — its type, approximate date, author assessment. 3–5 words.

**Body:** The translated text itself. Written as a historical document, not as game flavor text. The author's voice is present. It should be legible as something a real person wrote in a real situation.

**Length:**
- Skim-readable surface (what a 5-second glance conveys): one sentence
- Deep-read content (what 25–40 seconds reveals): the full document, including the detail that changes meaning

## BMS Consequence

After the tablet content, specify:
- What the Scholar's voice says during deep-read (one line, murmured — TDS drives this VO)
- BMS event generated on deep-read completion
- What warmth delta applies and why (which Vanguard cares about this tablet's content and why)
- Whether this tablet unlocks a puzzle consequence (e.g. Grand Armillary sequence from WA-003)

## Format

```
TABLET — [Room ID] — [Tablet ID]
Author: [Role/person]
Date: [Approximate period in Archive history]
Type: [Administrative record / Personal note / Emergency protocol / Philosophical argument / Other]

SKIM SURFACE (5 sec):
[One sentence — what a glancing reader takes away]

DEEP-READ CONTENT (25-40 sec):
[Full translated text — 3–8 sentences — in the author's voice]

SCHOLAR'S MURMUR (TDS VO — plays during deep-read):
"[What the Scholar says quietly as they translate — reveals their analytical process]"

BMS EVENT:
[Full RecordEvent call]

PUZZLE UNLOCK (if applicable):
[What this tablet enables elsewhere in the Archive]
```
