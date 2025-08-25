# Step-by-Step: Build, Simulate, Detect, Respond

> **Lab Scope:** All actions happen inside this repository. No real malware, no real phishing, no external network calls.

## Step 1 — Prepare the Lab
1. Use an isolated VM (Windows or Linux). Install Python 3.10+.
2. Clone or extract this repo. Create a virtual env and activate it.
3. Read `README.md` Safety Rails.

## Step 2 — Run Safe Attack Simulations (Red Team)
### 2.1 Phishing (Offline EML Generator)
- Generates realistic `.eml` messages and a CSV log. It does **not** send emails.
- Use cases: header analysis, training classifiers on **synthetic** phishing-like content.

**Run:**
```bash
python red_team/phishing_sim.py --generate-sample --targets sample_targets.csv --outdir sandbox/phishing_out
```

### 2.2 Ransomware-like Behavior (Non-destructive)
- Creates `sandbox/lab_data/` with dummy files.
- "Encrypts" by **renaming** and writing a marker header (**not real crypto**).
- Emits events to `logs/events.jsonl` for Blue Team detection.

**Run:**
```bash
python red_team/ransomware_behavior_sim.py --i-understand --files 50 --rate 200
```

### 2.3 Supply-chain Update Integrity Check
- Demonstrates manifest hashing and signature placeholder verification.
- Shows detection of a **tampered** update.

**Run:**
```bash
python red_team/supply_chain_update_sim/validate_update.py
```

## Step 3 — Detect (Blue Team)
1. Parse JSONL events and score anomalies:
   ```bash
   python blue_team/detection_scripts.py --watch logs/events.jsonl --threshold 30 --window 60
   ```
2. Review flags printed to console; confirm by reading `logs/alerts.jsonl`.

## Step 4 — Respond (Safely)
- Simulate host isolation and alerting:
  ```bash
  python blue_team/auto_response.py --simulate-isolation --send-alerts
  ```
- This only writes a file `sandbox/QUARANTINE_SIMULATED` and a console message.

## Step 5 — Monitoring
- Use `monitoring/logstash.conf` as a template if you forward events to ELK.
- Import `monitoring/kibana_dashboard.json` (placeholder) to build your detection views.

## Step 6 — Reporting
- Fill `docs/project_report.md` with your findings, screenshots, and metrics.
- Use `docs/incident_response_plan.md` and `docs/vendor_risk_checklist.md` for process maturity.

---

## Deliverables Checklist (GitHub)
- [ ] Repo with modules and docs
- [ ] Screenshots of Kibana/Splunk dashboards
- [ ] Sample alerts in `logs/alerts.jsonl`
- [ ] Clear disclaimers and safety rails

