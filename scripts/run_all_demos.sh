#!/usr/bin/env bash
set -euo pipefail
python red_team/phishing_sim.py --generate-sample --targets sample_targets.csv --outdir sandbox/phishing_out
python red_team/ransomware_behavior_sim.py --i-understand --files 25 --rate 200
python red_team/supply_chain_update_sim/validate_update.py
python blue_team/detection_scripts.py --watch logs/events.jsonl --threshold 20 --window 60
python blue_team/auto_response.py --simulate-isolation --send-alerts
echo "All demos complete."
