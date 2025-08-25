#!/usr/bin/env python3
"""
Supply-chain Update Integrity Demo:
- Verifies SHA256 against manifest.
- Compares 'tampered' artifact to demonstrate detection.
"""
import json, hashlib, os

BASE = os.path.dirname(__file__)
manifest_path = os.path.join(BASE, "update_manifest.json")

with open(manifest_path, "r", encoding="utf-8") as f:
    manifest = json.load(f)

good = os.path.join(BASE, manifest["artifact"])
tampered = os.path.join(BASE, "benign_app_v1.1.0_tampered.bin")

def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        while True:
            chunk = f.read(8192)
            if not chunk: break
            h.update(chunk)
    return h.hexdigest()

print("Verifying good artifact:", os.path.basename(good))
print("Expected:", manifest["sha256"])
print("Actual  :", sha256(good))

if manifest["sha256"] == sha256(good):
    print("OK: Good artifact matches manifest.")
else:
    print("FAIL: Good artifact hash mismatch.")

print("\nVerifying tampered artifact:", os.path.basename(tampered))
print("Expected:", manifest["sha256"])
print("Actual  :", sha256(tampered))

if manifest["sha256"] != sha256(tampered):
    print("DETECTED: Tampered artifact does not match manifest.")
else:
    print("WARNING: Tampered artifact unexpectedly matches (should not).")
