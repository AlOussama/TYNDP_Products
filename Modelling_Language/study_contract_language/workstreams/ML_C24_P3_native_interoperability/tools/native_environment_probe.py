#!/usr/bin/env python3
"""Non-normative native TOOL AVAILABILITY preflight; NOT a native language test."""
import importlib.util
import json
import shutil
import sys


def is_importable(name: str) -> bool:
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def main() -> None:
    report = {
        "run_id": "P3-ENV-20261123-r0.1",
        "python_version": sys.version.split()[0],
        "mathspec_package_available": is_importable("mathspec"),
        "gems_executable_path": shutil.which("gems") or None,
        "java_executable_path": shutil.which("java") or None,
        "sysml_pilot_parser_executable_path": shutil.which("sysml") or None,
        "native_tests_executed": False,
        "environment_probe_executed": True,
        "status": "NATIVE_NOT_EXECUTED",
        "interpretation": "A Java installation is not a SysML pilot parser. An absent package does not disprove native reuse.",
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
