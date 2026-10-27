# Aerospace - Workflow and Architecture

## Purchase order decisions

```mermaid
flowchart TD
    A["Create purchase order"] --> B["Created"]
    B --> C{"Approve?"}
    C -->|Yes| D["Approved"]
    C -->|Not yet| B
    D --> E["Record delivery"]
    E --> F["Delivered"]
    F --> G["Mark verified"]
    G --> H["Verified"]
    H --> I{"Audit event chain"}
    I -->|Valid| J["Report chain valid"]
    I -->|Invalid| K["Investigate changed history"]
```

The API rejects transitions that do not match the current state. There is no rejection, cancellation or partial-delivery workflow in this version. Audit failure returns a result; it does not automatically create a case or reverse the order status.

## Application components

```mermaid
flowchart TD
    U["Browser dashboard"] -->|"Read orders and metrics"| API["Python REST API"]
    U -->|"Submit workflow action"| API
    API --> W["Validate current status"]
    W --> DB["SQLite orders and events"]
    API --> V["Recalculate event hashes"]
    DB --> V
    V --> R["Return integrity result"]
    R --> U
```

## Event integrity check

```mermaid
flowchart TD
    A["Load order events by ID"] --> B["Start with GENESIS"]
    B --> C["Recalculate next event hash"]
    C --> D{"Hash and previous link match?"}
    D -->|No| E["Return invalid"]
    D -->|Yes| F{"More events?"}
    F -->|Yes| C
    F -->|No| G["Return valid for nonempty history"]
```

Hashed fields: order ID, action, actor, timestamp and previous hash. Quantity, part, supplier and unit cost are stored in the order table and are not protected by this event hash. Independent anchoring and detection of deleted suffixes are outside the current design.

## Repository visibility

The existing repository remains public. It contains a small demonstration implementation and synthetic seed data; no private core is needed for the present release. A future proprietary implementation or actual business data would require a private repository and a separately maintained public showcase. This decision does not change visibility on other projects.
