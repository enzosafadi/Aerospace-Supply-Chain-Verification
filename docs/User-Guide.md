# Aerospace - User Guide

## Install and run on Windows

Requires Python 3.9 or later. No third-party Python packages are needed.

Extract the project folder into `C:\Users\enzos\OneDrive\Documents`. Open a terminal in the extracted `Aerospace-Supply-Chain-Verification` folder, then run:

```powershell
python app.py
```

Open **http://localhost:8000**. Keep the terminal open while using the app. Stop it with Ctrl+C. `demo.sqlite3` is created locally and retains your demonstration changes.

If port 8000 is occupied:

```powershell
$env:PORT = '8001'
python app.py
```

The startup message prints the actual port. Open that address.

## Demonstration walkthrough

Review the three starting orders. Approve one, record delivery, then verify it. Select Audit to see `valid: true` and four events. Create an additional synthetic order to try the sequence yourself.

The application rejects out-of-sequence transitions through the API. The dashboard offers the next permitted action for each order. The audit result is displayed in a browser dialog.

## Understand the figures

Order Value is quantity multiplied by unit cost, summed across all current orders in CAD. It is not paid spend. Verified is a workflow state; it does not certify a component or prove an authenticated human approved it.

## Tests

```powershell
python -m unittest -v test_app.py
```

Tests use a separate temporary database and do not intentionally modify the demonstration database.

## Reset the demonstration

Stop the server. If you want to discard all local demonstration changes, delete `demo.sqlite3`, then restart the server. It will recreate the three baseline orders. Keep any records you want before resetting.

## Operating limits

Use synthetic data only. The application has no login or permissions, and its server binds to all interfaces. It is intended for a trusted local demonstration, not exposed internet hosting. There are no live supplier, ERP, blockchain or payment connections.

## Files for portfolio uploads

Use the thumbnail in `assets/thumbnails`, followed by SS1–SS3 once captured in `assets/screenshots`. These images show a demonstration; they do not represent real company results.

## Optional screenshot capture

With Node.js installed, run these in the project folder, in a second terminal while `python app.py` is running. This adds a development-only browser dependency; the Python application itself still requires only the standard library.

```powershell
npm install --no-save playwright
npx playwright install chromium
node tools/Capture-Screenshots.cjs
```

Use a fresh demonstration database for the expected three-order screenshots. The capture script advances synthetic orders 1 and 2; it checks the baseline before changing them.
