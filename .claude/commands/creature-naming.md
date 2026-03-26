---
description: Generate the Naming combat sequence for a creature type. The Naming tier is the highest combat action — permanent, costs only prior knowledge, requires a completed deep-read of the creature's origin inscription.
---

The user provides: the creature type (Fire-Warden / Lantern-Thief / Shadow-Walker / The Boundary / other), the room context, and whether the Scholar has already completed the relevant deep-read.

## The Naming System

Naming is Tier 3 combat — the highest tier. It requires:
1. The Scholar must have **completed a full deep-read** of the creature's origin inscription (TDS tracks this — `isOriginRead == true`)
2. The Scholar speaks the designation in the Naming Tongue (Avestan — an academic skill, not supernatural)
3. The creature becomes **permanently non-hostile in that category** (not just this instance — all creatures of this type in rooms the Scholar has Named)

**What Naming costs:** Only time and prior reading. No oil, no bolts, no bells.
**What Naming cannot do:** It cannot Name the Boundary. (Bells stun it for 8 seconds — that is the maximum.)

## Creature Voice Guide (for the Naming line)

Each creature type has a Naming designation — the formal Avestan name from the Archive's founding records. The Scholar speaks this designation after the deep-read. It is not a magic word — it is the correct administrative name for the thing, spoken by someone who has earned the right to speak it through study.

**Fire-Warden (Yazata):** Designation root: "Atash-Yazata-[chamber-number]". The Scholar speaks the chamber assignment — the Warden was assigned to a specific space, and its name includes that space. Naming it reminds it of its original function.

**Lantern-Thief (Pairika):** Designation root: "Pairika-[cold-light-frequency]". The Scholar names the frequency of cold light the creature was drawn from. Naming it is categorization — the Scholar places the creature correctly in the Archive's own taxonomy.

**Shadow-Walker (Daeva):** Designation root: "Daeva-[directional-commitment]". These beings committed to the wrong direction at creation. The Scholar names the direction. This does not change them — it acknowledges them correctly.

## Generate

**1. The origin inscription** — 3–4 lines of translated Avestan text the Scholar reads during the deep-read, explaining what this creature is and how the Archive's founders categorized it. Written as academic record, not as a warning.

**2. The Naming sequence script** (for `NamingCombatController.cs`):

```csharp
public IEnumerator ExecuteNaming(CreatureType type, string roomId)
{
    // 1. Verify deep-read completed (TDSController check)
    // 2. Scholar speaks designation (VO trigger — actual Avestan phrase)
    // 3. Creature state transition: hostile → designated
    // 4. BMSEvent: Scholar used Naming tier (significant BMS record)
    // 5. Permanent registry update: NamingRegistry.Register(type, roomId)
}
```

**3. BMS event** — Naming is a significant scholarly action. Generate the full `RecordEvent` call with appropriate warmth deltas. Both Vanguards care about this: it demonstrates that the Scholar's reading practice has depth consequences.

**4. The Dark Voice line** (if first time Scholar Names a creature of this type):
A single line, beside or ahead origin, noting what the Scholar just did in Fan Li/Sun Tzu vocabulary.
