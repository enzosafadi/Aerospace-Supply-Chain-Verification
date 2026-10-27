# Aerospace - Business Case

## Why I built this prototype

A purchase order can look complete in a spreadsheet while its supporting history remains difficult to reconstruct. A buyer may know the supplier has delivered; an operations manager may still need to know who approved the order, whether the steps happened in sequence, and whether the recorded history has changed.

I built this project to examine that narrower problem: how a small application can make a procurement workflow easier to inspect and provide a basic check on the integrity of its event history. Aerospace is the demonstration context because the connection between a purchased component and its records is an important business concern. This prototype does not establish airworthiness or regulatory compliance.

## The operating problem

In a hypothetical procurement team, order information is split between a tracker, messages and individual recollections. The team can spend time reconciling status and cannot consistently explain why an order moved forward. A manager reviewing an exception needs a usable history, rather than another total on a dashboard.

The case therefore centres on three needs: a defined sequence of actions, a persistent order record, and a repeatable way to check recorded events. These are design assumptions for a portfolio scenario, not findings from a client engagement.

## Who benefits

| User | Need | What the prototype provides |
|---|---|---|
| Buyer | See which orders need the next action | Current order status and an action appropriate to that status |
| Operations manager | Review purchasing exposure and progress | Order count, verified count and total order value |
| Internal reviewer | Check the consistency of recorded history | Per-order SHA-256 chain verification |
| Technical reviewer | Understand and reproduce the controls | Python source, documented API and four automated tests |

A president could use the overview to start a management discussion: how much purchasing value is represented, how many orders reached the final workflow stage, and which orders remain unfinished. This version does not provide supplier performance, profitability, delivery timeliness or cash-flow analytics.

## Options considered

| Option | Advantage | Limitation |
|---|---|---|
| Keep a shared spreadsheet | Familiar and inexpensive to start | Workflow and event-history controls depend on manual discipline |
| Configure an existing ERP workflow | Fits an established enterprise environment | Requires the organisation's systems, permissions and implementation effort |
| Build a small local prototype | Makes the proposed sequence and verification logic directly testable | Does not supply enterprise identity, independent audit custody or production resilience |

I selected the local prototype for this portfolio exercise because the control logic can be inspected without an ERP subscription or an external network. In an actual company, extending the existing ERP would need serious consideration before commissioning a separate application.

## Proposed approach

An order moves from Created to Approved, Delivered and Verified. Each permitted action creates an event with an actor label, a UTC timestamp and a link to the preceding event hash. An independent audit action recalculates the stored event chain.

The distinction matters: **Verified is a workflow status; a valid audit result is a separate integrity check.** Neither proves that a physical component is authentic, that the stated actor is authenticated, or that the purchase is commercially justified.

## What is demonstrated

The initial scenario contains three synthetic orders worth **CA$25,478.50**. The application supports creation, controlled transitions, persistence and chain checking. Four automated tests pass: creation, a complete workflow, rejection of an out-of-sequence action, and detection of a changed event actor field.

Those are functional observations, not evidence of business savings. No reduction in processing time, errors or audit cost has been measured.

## How a pilot would be evaluated

Before a real pilot, I would document the existing approval process, authority limits, required evidence and exceptions with procurement and internal control stakeholders. Baseline measures would include time to reconstruct one order history, incorrect transitions, incomplete records and time to resolve exceptions.

The pilot should process equivalent scenarios through the existing process and the proposed workflow. Successful adoption would require users to retrieve the expected history, reproduce every required step, reject all agreed invalid transitions and explain any integrity failure. Time or cost benefits should be reported only after measuring the baseline and pilot on comparable work.

Financial evaluation would compare implementation, integration, training and ongoing support costs with measured staff time saved and evidenced avoidable rework. There is no defensible ROI figure until those inputs exist.

## Risks and limits that affect the decision

The local database is the single source of both records and hashes. Someone with database write access could rewrite a chain or delete trailing events without an independent checkpoint detecting that change. Order fields such as quantity and price are not included in the hashed event payload. Actor names are labels, not verified identities.

These limits make this an educational control prototype, not an enterprise audit service. A production decision would require identity and permissions, independently retained integrity checkpoints, stronger data validation, concurrency controls, backups and security review. Aerospace certification documents and quality approvals would need their own designed controls.

## Recommendation

Keep this version as a reproducible portfolio demonstration of workflow analysis and tamper-evident event recording. Use it to discuss requirements and control trade-offs. Advance to a real company pilot only after the process owner has agreed the required controls and an integration assessment has shown that a separate application is justified.
