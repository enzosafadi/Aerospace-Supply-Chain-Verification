"""Local aerospace supply-chain workflow and verification prototype."""
import hashlib
import json
import sqlite3
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
DB = ROOT / "demo.sqlite3"

def connect():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def initialize():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY,
            supplier TEXT NOT NULL,
            part TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity > 0),
            unit_cost REAL NOT NULL CHECK(unit_cost >= 0),
            status TEXT NOT NULL DEFAULT 'created'
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            order_id INTEGER NOT NULL REFERENCES orders(id),
            action TEXT NOT NULL,
            actor TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            previous_hash TEXT NOT NULL,
            event_hash TEXT NOT NULL
        );
        """)

def hash_event(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()

def record(conn, order_id, action, actor):
    previous = conn.execute(
        "SELECT event_hash FROM events WHERE order_id=? ORDER BY id DESC LIMIT 1",
        (order_id,)
    ).fetchone()
    payload = dict(order_id=order_id, action=action, actor=actor,
                   timestamp=datetime.now(timezone.utc).isoformat(),
                   previous_hash=previous["event_hash"] if previous else "GENESIS")
    digest = hash_event(payload)
    conn.execute(
        "INSERT INTO events(order_id,action,actor,timestamp,previous_hash,event_hash) VALUES(?,?,?,?,?,?)",
        (*payload.values(), digest)
    )
    return digest

def create_order(data):
    supplier = str(data["supplier"]).strip()
    part = str(data["part"]).strip()
    quantity = int(data["quantity"])
    unit_cost = float(data["unit_cost"])
    if not supplier or not part or quantity <= 0 or not 0 <= unit_cost < 1e12:
        raise ValueError("Invalid order details")
    with connect() as conn:
        cursor = conn.execute(
            "INSERT INTO orders(supplier,part,quantity,unit_cost) VALUES(?,?,?,?)",
            (supplier, part, quantity, unit_cost)
        )
        record(conn, cursor.lastrowid, "created", "system")
        return dict(id=cursor.lastrowid, status="created")

def advance(order_id, action, actor="operator"):
    steps = {"approve": ("created", "approved"),
             "deliver": ("approved", "delivered"),
             "verify": ("delivered", "verified")}
    if action not in steps:
        raise ValueError("Unknown action")
    before, after = steps[action]
    with connect() as conn:
        row = conn.execute("SELECT status FROM orders WHERE id=?", (order_id,)).fetchone()
        if row is None or row["status"] != before:
            raise ValueError("Invalid workflow transition")
        conn.execute("UPDATE orders SET status=? WHERE id=?", (after, order_id))
        digest = record(conn, order_id, action, actor)
    return dict(id=order_id, status=after, event_hash=digest)

def verify_history(order_id):
    with connect() as conn:
        events = conn.execute(
            "SELECT * FROM events WHERE order_id=? ORDER BY id", (order_id,)
        ).fetchall()
    previous = "GENESIS"
    for event in events:
        payload = {k: event[k] for k in
                   ("order_id", "action", "actor", "timestamp", "previous_hash")}
        if event["previous_hash"] != previous or hash_event(payload) != event["event_hash"]:
            return dict(valid=False, events=len(events))
        previous = event["event_hash"]
    return dict(valid=bool(events), events=len(events))

def list_orders():
    with connect() as conn:
        return [dict(row) for row in conn.execute(
            "SELECT *, ROUND(quantity*unit_cost,2) AS total FROM orders ORDER BY id DESC"
        )]

class API(BaseHTTPRequestHandler):
    def respond(self, status, payload):
        body = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/":
            body = (ROOT / "dashboard.html").read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif path == "/api/orders":
            self.respond(200, list_orders())
        elif path == "/api/metrics":
            orders = list_orders()
            self.respond(200, dict(count=len(orders),
                                   verified=sum(o["status"] == "verified" for o in orders),
                                   value=round(sum(o["total"] for o in orders), 2)))
        elif path.startswith("/api/orders/") and path.endswith("/verify"):
            try:
                self.respond(200, verify_history(int(path.split("/")[3])))
            except ValueError:
                self.respond(400, {"error": "Invalid order ID"})
        else:
            self.respond(404, {"error": "Not found"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 0 or length > 100000:
                raise ValueError("Invalid payload size")
            data = json.loads(self.rfile.read(length))
            parts = urlparse(self.path).path.strip("/").split("/")
            if parts == ["api", "orders"]:
                result = create_order(data)
            elif len(parts) == 4 and parts[:2] == ["api", "orders"]:
                result = advance(int(parts[2]), parts[3], str(data.get("actor", "operator"))[:80])
            else:
                raise ValueError("Unknown endpoint")
            self.respond(201, result)
        except (ValueError, KeyError, TypeError) as exc:
            self.respond(400, {"error": str(exc)})

if __name__ == "__main__":
    initialize()
    if not list_orders():
        for supplier, part, qty, price in [
            ("Northstar Components", "ACT-204", 12, 845.50),
            ("Aero Precision", "VAL-918", 8, 1220),
            ("Summit Aerospace", "BRK-105", 30, 185.75),
        ]:
            create_order(dict(supplier=supplier, part=part, quantity=qty, unit_cost=price))
    port = int(__import__("os").environ.get("PORT", 8000))
    print(f"Open http://localhost:{port}")
    ThreadingHTTPServer(("0.0.0.0", port), API).serve_forever()

