#!/usr/bin/env python3
"""M2-D-SOURCE1: fail-closed public OSM v0.6 acquisition and limited topology witness.

Only publish the resulting JSON after reviewing license and source admissibility.
No operational dispatch, N-1, official IoSN or TSO gate is certified here.
"""
import argparse
import collections
import csv
import hashlib
import json
import math
import pathlib
import urllib.request
from datetime import datetime, timezone

RECORD = "14144752"
FILENAMES = ("buses.csv", "lines.csv", "links.csv", "transformers.csv", "converters.csv")
PUBLISHED_MD5 = {
    "buses.csv": "6b6059dca66ce5851bef4be06460bc23",
    "lines.csv": "aa4ad8a608323358db2e866430f33458",
    "links.csv": "19a92e63b8788c931b227ea796f9abff",
    "transformers.csv": "b48673b9152e16324ef155ae7a9b0365",
    "converters.csv": "89cdb6dc392bc272a4bf14ba4eb1255d",
}
QUOTA_GIT_BLOB = "e147ba7143ecc21647055d9413f0973338a25b0f"


def digest(raw, algorithm):
    return hashlib.new(algorithm, raw).hexdigest()


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as stream:
        return list(csv.DictReader(stream))


def audit_quota(path):
    raw = path.read_bytes()
    git_blob = digest(f"blob {len(raw)}\0".encode() + raw, "sha1")
    rows = read_csv(path)
    names = [r["country_label_as_published"] for r in rows]
    valid = (git_blob == QUOTA_GIT_BLOB and len(rows) == 37 and
             sum(int(r["n_zones"]) for r in rows) == 102 and
             len(names) == len(set(names)) and
             "Northern Ireland" in names and "United Kingdom" in names)
    return {"status": "PASS_LIMITED_SOURCE_TABLE" if valid else "FAIL",
            "git_blob_sha1": git_blob, "sha256": digest(raw, "sha256"),
            "byte_length": len(raw), "row_count": len(rows),
            "quota_total": sum(int(r["n_zones"]) for r in rows),
            "northern_ireland_and_uk_distinct": "Northern Ireland" in names and "United Kingdom" in names}


def acquire(out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest = {"record": RECORD, "version": "0.6", "license": "ODbL-1.0",
                "producer": "Xiong et al. / PyPSA-Eur / OSM contributors",
                "source_uri": f"https://zenodo.org/records/{RECORD}",
                "acquired_utc": datetime.now(timezone.utc).isoformat(), "files": []}
    for name in FILENAMES:
        url = f"https://zenodo.org/records/{RECORD}/files/{name}?download=1"
        path = out_dir / name
        if not path.exists():
            req = urllib.request.Request(url, headers={"User-Agent": "M2-D-SOURCE1-qualifier/1.0"})
            with urllib.request.urlopen(req, timeout=120) as response, path.open("wb") as output:
                while True:
                    chunk = response.read(1048576)
                    if not chunk:
                        break
                    output.write(chunk)
        raw = path.read_bytes()
        md5 = digest(raw, "md5")
        item = {"name": name, "source_uri": url, "bytes": len(raw),
                "md5_published": PUBLISHED_MD5[name], "md5_computed": md5,
                "sha256_original_bytes": digest(raw, "sha256"),
                "status": "PASS_ORIGINAL_BYTES" if md5 == PUBLISHED_MD5[name] else "FAIL_MD5_MISMATCH"}
        manifest["files"].append(item)
        if md5 != PUBLISHED_MD5[name]:
            raise ValueError(f"Fail-closed: published Zenodo MD5 mismatch: {name}")
    (out_dir / "source_manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return manifest


def is_dc(value):
    return str(value).strip().lower() in {"true", "t", "1", "yes"}


def find_cycle(buses, edges, max_nodes=24):
    """Find a real two-country, >=3-bus AC cycle including an AC border branch."""
    adj = collections.defaultdict(list)
    for edge in edges:
        a, b = edge["bus0"], edge["bus1"]
        if a in buses and b in buses and a != b:
            adj[a].append((b, edge["id"]))
            adj[b].append((a, edge["id"]))
    candidates = sorted((e for e in edges if e["bus0"] in buses and e["bus1"] in buses and
                        buses[e["bus0"]] != buses[e["bus1"]]), key=lambda e: e["id"])
    best = None
    for edge in candidates:
        start, target = edge["bus0"], edge["bus1"]
        pair = {buses[start], buses[target]}
        queue = collections.deque([(start, (start,))])
        visited = {start}
        while queue:
            node, path = queue.popleft()
            if len(path) >= max_nodes:
                continue
            for neighbor, edge_id in adj[node]:
                if edge_id == edge["id"] or buses[neighbor] not in pair:
                    continue
                if neighbor == target and len(path) >= 2:
                    cycle = path + (target,)
                    if len(cycle) >= 3 and (best is None or len(cycle) < len(best[0])):
                        best = (cycle, edge["id"], sorted(pair))
                    break
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + (neighbor,)))
    return best


def audit_topology(raw_dir):
    buses_rows = read_csv(raw_dir / "buses.csv")
    lines_rows = read_csv(raw_dir / "lines.csv")
    other_rows = {name: read_csv(raw_dir / f"{name}.csv")
                  for name in ("links", "transformers", "converters")}
    required = {"bus_id", "country", "dc", "voltage"}
    if not buses_rows or not required.issubset(buses_rows[0]):
        raise ValueError("Unsupported buses.csv schema")
    if not lines_rows or not {"line_id", "bus0", "bus1", "x", "voltage"}.issubset(lines_rows[0]):
        raise ValueError("Unsupported lines.csv schema / x unit missing")
    identifiers = [r["bus_id"] for r in buses_rows]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Duplicate bus IDs in source")
    all_bus_ids = set(identifiers)
    buses = {r["bus_id"]: r["country"].strip() for r in buses_rows if
             r["bus_id"] and r["country"] and not is_dc(r["dc"])}
    ids = set()
    valid_lines, invalid_lines = [], []
    for r in lines_rows:
        name = r["line_id"]
        if not name or name in ids:
            raise ValueError("Missing/duplicate line ID")
        ids.add(name)
        if r["bus0"] not in all_bus_ids or r["bus1"] not in all_bus_ids:
            invalid_lines.append({"id": name, "reason": "UNKNOWN_ENDPOINT"})
            continue
        try:
            x_ohm, voltage = float(r["x"]), float(r["voltage"])
        except (TypeError, ValueError):
            invalid_lines.append({"id": name, "reason": "MISSING_X_OR_VOLTAGE"})
            continue
        if not (math.isfinite(x_ohm) and x_ohm > 0 and math.isfinite(voltage) and voltage > 0):
            invalid_lines.append({"id": name, "reason": "NONPOSITIVE_X_OR_VOLTAGE"})
            continue
        if r["bus0"] in buses and r["bus1"] in buses:
            valid_lines.append({"id": name, "bus0": r["bus0"], "bus1": r["bus1"],
                                "x_ohm": x_ohm, "voltage_kv": voltage})
    cycle = find_cycle(buses, valid_lines)
    result = {"source_kind": "OSM_RECONSTRUCTED_OPEN_TOPOLOGY", "tsovalidated": False,
              "status": "BLOCKED", "bus_count": len(buses_rows),
              "line_count": len(lines_rows), "accepted_ac_line_count": len(valid_lines),
              "excluded_source_lines": invalid_lines,
              "device_table_counts": {k: len(v) for k, v in other_rows.items()},
              "parameter_quality": "HEURISTIC_OPEN_DATA",
              "dispatch_available": False, "reference_flow_oracle_available": False,
              "seasonal_ratings_available": False, "security_available": False,
              "equipment_policy": "Non-line devices NOT represented in this limited line-only extraction"}
    if cycle:
        nodes, tie_id, pair = cycle
        node_set = set(nodes)
        induced = [e for e in valid_lines if e["bus0"] in node_set and e["bus1"] in node_set]
        # A graph-cycle alone does not qualify the subset's transformer/HVDC equipment completeness.
        induced_other = []
        for name, rows in other_rows.items():
            for r in rows:
                if r.get("bus0") in node_set and r.get("bus1") in node_set:
                    induced_other.append({"table": name, "id": next((r[k] for k in r if k.endswith("_id")), None)})
        result["two_country_candidate"] = {"countries": pair, "bus_ids": list(nodes),
            "ac_cross_border_line_id": tie_id, "induced_ac_branches": [e["id"] for e in induced],
            "other_induced_devices": induced_other,
            "test_base_mva": 100.0,
            "electrical_parameter_conversion": "x_pu=x_ohm*100/(voltage_kv**2); test-base only",
            "x_pu_by_line": {e["id"]: e["x_ohm"] * 100.0 / (e["voltage_kv"]**2)
                             for e in induced},
            "boundary_truncation": "Other edges incident to selected buses exist outside extracted witness; not a closed physical real-grid model"}
        result["status"] = ("PARTIAL_REAL_TOPOLOGY_WITNESS" if not induced_other
                            else "BLOCKED_INDUCED_SPECIAL_EQUIPMENT")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quota", type=pathlib.Path)
    ap.add_argument("--raw-dir", type=pathlib.Path)
    ap.add_argument("--acquire", action="store_true")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    result = {"tool": "M2-D-SOURCE1-v1", "real_grid_approved": False}
    if args.quota:
        result["quota"] = audit_quota(args.quota)
    if args.self_test:
        example_buses = {"A": "AT", "B": "AT", "C": "DE"}
        example_edges = [{"id": "s1", "bus0": "A", "bus1": "B"},
                         {"id": "s2", "bus0": "B", "bus1": "C"},
                         {"id": "s3", "bus0": "C", "bus1": "A"}]
        example = find_cycle(example_buses, example_edges)
        result["synthetic_algorithm_test"] = "PASS" if example and len(example[0]) == 3 else "FAIL"
    if args.raw_dir:
        if args.acquire or all((args.raw_dir / name).exists() for name in FILENAMES):
            # Even locally cached files must be re-hashed and matched to published MD5.
            result["acquisition"] = acquire(args.raw_dir)
            result["topology"] = audit_topology(args.raw_dir)
        else:
            result["topology"] = {"status": "BLOCKED_ORIGINAL_FILES_NOT_PRESENT"}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
