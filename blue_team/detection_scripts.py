#!/usr/bin/env python3
"""
Detection Scripts:
- Reads JSONL events from logs/events.jsonl.
- Flags bursts of rename_locked actions (threshold within rolling time window).
- Writes alerts to logs/alerts.jsonl.
"""
import argparse, json, datetime, collections, os, sys

def parse_ts(s):
    return datetime.datetime.fromisoformat(s.replace("Z","+00:00"))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--watch", default="logs/events.jsonl")
    ap.add_argument("--threshold", type=int, default=20, help="Min events within window to alert")
    ap.add_argument("--window", type=int, default=60, help="Seconds for rolling window")
    args = ap.parse_args()

    if not os.path.exists(args.watch):
        print(f"No events file at {args.watch}")
        sys.exit(1)

    with open(args.watch, "r", encoding="utf-8") as f:
        lines = [json.loads(x) for x in f if x.strip()]

    q = collections.deque()
    alerts = []
    for ev in lines:
        if ev.get("module") != "ransomware_sim" or ev.get("action") != "rename_locked":
            continue
        t = parse_ts(ev["ts"])
        q.append(t)
        # evict old
        while q and (t - q[0]).total_seconds() > args.window:
            q.popleft()
        if len(q) >= args.threshold:
            alert = {
                "ts": ev["ts"],
                "type": "ransomware_burst_detected",
                "count": len(q),
                "window_s": args.window,
                "note": "High rate of file renames consistent with ransomware-like behavior (simulation)."
            }
            alerts.append(alert)

    if alerts:
        os.makedirs("logs", exist_ok=True)
        with open("logs/alerts.jsonl", "a", encoding="utf-8") as af:
            for a in alerts:
                af.write(json.dumps(a) + "\n")
        print(f"Alerts written: {len(alerts)} -> logs/alerts.jsonl")
    else:
        print("No bursts detected with current parameters.")

if __name__ == "__main__":
    main()
