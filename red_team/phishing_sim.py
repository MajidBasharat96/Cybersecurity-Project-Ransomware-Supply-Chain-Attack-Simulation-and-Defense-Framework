#!/usr/bin/env python3
"""
Phishing Simulator (Safe): Generates .eml files and logs, does not send email.
"""
import os, csv, argparse, datetime, random, string, json, pathlib

TEMPLATES = [
    ("Password Reset Required", "We noticed a sign-in attempt. Reset your password within 24 hours to avoid lockout."),
    ("Invoice Overdue", "Your invoice is overdue. View the statement in the attached portal link."),
    ("HR Policy Update", "We updated our remote work policy. Review and acknowledge by Friday."),
]

def rand_id(n=8):
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(n))

def make_eml(sender, recipient, subject, body):
    now = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S +0000")
    msg = f"""From: {sender}
To: {recipient}
Subject: {subject}
Date: {now}
MIME-Version: 1.0
Content-Type: text/html; charset=UTF-8

<html><body>
<p>{body}</p>
<p><b>[SIMULATION ONLY]</b> This message is generated for training/log analysis.</p>
</body></html>
"""
    return msg

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", required=True, help="CSV with column 'email'")
    ap.add_argument("--outdir", default="sandbox/phishing_out")
    ap.add_argument("--generate-sample", action="store_true", help="Create a sample targets CSV if not present")
    args = ap.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    os.makedirs("logs", exist_ok=True)

    if args.generate_sample and not os.path.exists(args.targets):
        with open(args.targets, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["email"])
            w.writeheader()
            for i in range(10):
                w.writerow({"email": f"user{i}@example.com"})

    # Load targets
    targets = []
    with open(args.targets, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if "email" in row and row["email"]:
                targets.append(row["email"])

    log_path = "logs/events.jsonl"
    sent_log = []
    for rcp in targets:
        subject, body = random.choice(TEMPLATES)
        mid = rand_id()
        eml = make_eml("it-support@example.com", rcp, subject, body)
        path = os.path.join(args.outdir, f"{mid}.eml")
        with open(path, "w", encoding="utf-8") as f:
            f.write(eml)

        event = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "module": "phishing_sim",
            "recipient": rcp,
            "message_id": mid,
            "subject": subject,
            "path": path,
            "note": "SIMULATION_ONLY_NO_EMAIL_SENT"
        }
        with open(log_path, "a", encoding="utf-8") as lf:
            lf.write(json.dumps(event) + "\n")
        sent_log.append(event)

    print(f"Generated {len(sent_log)} .eml files in {args.outdir}. Logged to logs/events.jsonl")

if __name__ == "__main__":
    main()
