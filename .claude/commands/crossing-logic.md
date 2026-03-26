---
description: Generate or review traversal focal point (TFP) crossing logic for a specific room pair. Enforces the Iron Rule and traversal debt system.
---

The user provides: the room ID pair (e.g. WA-003 ↔ WB-004), any special conditions (one-way, restricted, requires item), and whether this TFP is used in a specific puzzle.

## Iron Rule Verification (do this first)

Before generating code, state clearly:
- What World B knowledge will this crossing enable in World A?
- What World A material will produce physical change in World B?

If the crossing serves no Iron Rule purpose in the context provided, flag this before proceeding.

## Generate: TraversalFocalPoint component for this room pair

The crossing must implement:

**1. The "look before you commit" mechanic (SH4 model)**
Scholar approaches TFP and sees the other world through the ring — inverted/distorted — before committing. Player must confirm. Show what the Scholar sees: `PeekView()` that renders the destination world through the ring's viewport.

**2. Traversal debt increment**
```csharp
WorldManager.Instance.traversalDebt++;
BMSController.Instance.RecordEvent(new BMSEvent {
    eventType = BMSEventType.Crossing,
    tag = BMSEventTags.VOLUNTARY_CROSSING,
    // voluntaryness, destination world, debt at time of crossing
});
```

**3. Boundary spawn check**
- Debt 2: 8-second manifestation (establishing dread — Scholar not in danger)
- Debt 3: 20-second pursuit
- Debt 4+: Persistent until next fire altar save

**4. The 2.2-second non-interruptable transition**
No input accepted during crossing. Scholar's fire vessel dims on WB entry (cold world, no warmth). Scholar's fire vessel brightens on WA return.

**5. World swap**
Disable current `WorldRoot`, enable destination `WorldRoot`, swap camera set, swap audio mix.

## Output Format

Full `TraversalFocalPoint.cs` for this specific room pair. Include:
- Room IDs as `[SerializeField]` strings
- All debt logic
- Iron Rule comment at top: what knowledge flows which direction through this TFP
- `[Header]` attributes grouping inspector fields by: Room Config / Debt Config / Audio / Visual

Then: a one-line note on whether the Scholar can undo this crossing (always yes — they can cross back) and what it costs (another debt increment, always).
