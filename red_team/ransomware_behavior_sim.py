#!/usr/bin/env python3
"""
Ransomware-like Behavior Simulator (Safe).
- Operates ONLY in sandbox/lab_data created by this script.
- Non-destructive: creates dummy files then renames/marks them.
- Emits JSON events to logs/events.jsonl.
"""
import os, argparse, datetime, time, json, random, string, pathlib, sys

BANNER = "THIS_IS_A_SIMULATED_RANSOMWARE_NOTE—EDU_ONLY"

def gen_dummy_text(n=1024):
    return "".join(random.choice(string.ascii_letters + string.digits + " ") for _ in range(n))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--i-understand", action="store_true", help="Acknowledge safety notice")
    ap.add_argument("--files", type=int, default=25, help="Number of dummy files to create")
    ap.add_argument("--rate", type=int, default=100, help="Approx ops per minute (rename speed)")
    args = ap.parse_args()

    if not args.i_understand:
        print("Refusing to run without --i-understand")
        sys.exit(1)

    base = "sandbox/lab_data"
    os.makedirs(base, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    # Create dummy files if none exist
    created = 0
    for i in range(args.files):
        p = os.path.join(base, f"doc_{i:03d}.txt")
        if not os.path.exists(p):
            with open(p, "w", encoding="utf-8") as f:
                f.write(gen_dummy_text(2048))
            created += 1

    # Ransom note
    note = os.path.join(base, "READ_ME_RESTORE_FILES.txt")
    with open(note, "w", encoding="utf-8") as f:
        f.write(BANNER + "\nThis is a harmless, educational simulation.\n")

    # Rename dummy files to simulate "encryption"
    files = [os.path.join(base, x) for x in os.listdir(base) if x.endswith(".txt")]
    delay = 60 / max(args.rate, 1)
    ops = 0
    for p in files:
        newp = p + ".locked.sim"
        os.rename(p, newp)
        ops += 1
        event = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "module": "ransomware_sim",
            "action": "rename_locked",
            "old_path": p,
            "new_path": newp
        }
        with open("logs/events.jsonl", "a", encoding="utf-8") as lf:
            lf.write(json.dumps(event) + "\n")
        time.sleep(delay)

    # Final event
    with open("logs/events.jsonl", "a", encoding="utf-8") as lf:
        lf.write(json.dumps({
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "module": "ransomware_sim",
            "action": "note_created",
            "path": note,
            "banner": BANNER
        }) + "\n")
    print(f"Simulation complete. Created {created} files, renamed {ops}, wrote ransom note at {note}.")

if __name__ == "__main__":
    main()
