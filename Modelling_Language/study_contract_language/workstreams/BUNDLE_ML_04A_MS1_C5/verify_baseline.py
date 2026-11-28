"""Verify actual Git tree bytes against connector-fetched C4 pins."""
import json,subprocess
from pathlib import Path
p=Path(__file__).with_name("source_baseline.json")
manifest=json.loads(p.read_text())
for row in manifest["c4_artifacts"]:
    got=subprocess.check_output(["git","hash-object",row["path"]],text=True).strip()
    historical=subprocess.check_output(["git","rev-parse",manifest["c4_head"]+":"+row["path"]],text=True).strip()
    if got!=row["blob"] or historical!=row["blob"]:raise SystemExit("C4_BLOB_MISMATCH:"+row["path"])
print("C5_BASELINE_PINS="+str(len(manifest["c4_artifacts"]))+" exact original C4 blobs")
