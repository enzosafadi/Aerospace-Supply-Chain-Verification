# Aerospace - Project Presentation

## The project in plain language

This is a small working application for following a purchase order through creation, approval, delivery and verification. It combines an operations dashboard with a persistent event history, so a reviewer can inspect progress and check whether stored event values still match their hashes.

It addresses a hypothetical procurement team's difficulty in connecting order status with a consistent history. All suppliers, parts, orders and amounts are synthetic. It is a portfolio demonstration, not a client deployment.

## From beginning to end

1. Run the local Python service. It creates a SQLite database and three sample orders on first launch.
2. Open the dashboard. Review order count, verified count and total purchase order value.
3. Create an order using supplier, part number, quantity and unit cost.
4. Approve it. Attempting delivery before approval is rejected by the workflow engine.
5. Record delivery and then mark the order Verified. Each step records an event.
6. Select Audit on a verified order. The application recalculates its chain and returns validity and event count.

A fully processed order has four events: creation, approval, delivery and verification. The dashboard supplies the actor label `demo-operator` for actions; it does not authenticate the person using the browser.

## Management use

A president can use the dashboard as the beginning of an exception discussion: which purchases remain unfinished, what value they represent, and whether a completed order's event chain passes its check. The buyer executes the steps; management reviews the evidence and asks what is blocking progress.

Order value represents the sum of recorded quantities multiplied by unit cost. It is not expenditure paid, revenue or profit. The Verified count means orders at the final workflow stage, not certified components or independently validated suppliers.

## What the business gains if a future pilot succeeds

The intended benefit is a more consistent record and less effort reconstructing a purchase's progression. These benefits are hypotheses. This demonstration establishes functioning controls, not measured improvements in a real business.

## Read next

- [Business case](../Business-Case.md): rationale, alternatives, beneficiaries and evaluation.
- [Workflow and architecture](Workflow-And-Architecture.md): diagrams and controls.
- [User guide](User-Guide.md): installation, walkthrough and troubleshooting.
- [Validation](Validation.md): actual checks and limitations.
