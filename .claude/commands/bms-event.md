---
description: Scaffold a new BMS event type with correct struct fields, warmth delta logic, and registration in BMSController. Use whenever a new observable Scholar behavior needs to feed the behavioral model.
---

The user will provide:
1. A description of the Scholar behavior to record (e.g. "Scholar reads a creature origin inscription aloud before combat")
2. Which Vanguard(s) it's relevant to (VA, VB, or both)
3. The approximate warmth impact (small / medium / large, or explicit delta values)

## What To Generate

**1. A `BMSEventType` enum entry** — derive a `SCREAMING_SNAKE_CASE` tag from the behavior description. Add to `BMSEventType.cs`.

**2. A `BMSEvent` struct instance** — fully populated, ready to pass to `BMSController.Instance.RecordEvent()`.

**3. The call site** — where in the codebase this event should be dispatched. Identify the correct MonoBehaviour and method. The call must happen at the moment the behavior is *completed*, not initiated.

**4. A one-line comment** explaining why this behavior is meaningful to the Vanguard's model.

## Rules

- Warmth deltas must be **integers** clamped to the range −20 to +20 in BMSController
- Small impact: ±1–2 | Medium: ±3–5 | Large: ±6–8 | Maximum (like Translation Obelisk): ±10
- `wa_warmthDelta` and `vb_warmthDelta` are independent — a behavior can warm VA while cooling VB
- Events are batched **per room-session**, not per frame — do not generate events on `Update()`
- The event tag (`string tag`) must match a `const string` in `BMSEventTags.cs` — generate that constant too
- **Never** generate any UI notification, Debug.Log of warmth values, or player-facing feedback alongside the event

## Output Format

```csharp
// BMSEventTags.cs — add this constant
public const string [TAG_NAME] = "[TAG_VALUE]";

// BMSEventType.cs — add this enum value  
[EventTypeName],   // [one-line explanation of what this captures about the Scholar]

// Call site: [ClassName.cs → MethodName()]
BMSController.Instance.RecordEvent(new BMSEvent {
    eventType    = BMSEventType.[EventTypeName],
    tag          = BMSEventTags.[TAG_NAME],
    wa_warmthDelta = [value],   // [why VA cares about this]
    vb_warmthDelta = [value],   // [why VB cares about this]
    roomId       = currentRoomId,
    sessionTime  = sessionTimer
});
```

Then: one paragraph explaining what behavioral change this event will eventually produce in the Vanguard once the warmth threshold moves — written as the Vanguard would understand it, not as a game system description.
