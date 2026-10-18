#!/usr/bin/env python3
"""Run every local CPU smoke test and the revised stress comparison."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[1] / "src"))
from stress_simulator import StressEngine, StressSession


def main():
    root = Path(__file__).parents[1]
    tests = sorted((root / "tests").glob("test_*.py"))
    for test in tests:
        subprocess.run([sys.executable, str(test)], check=True)
    sessions = [StressSession(i, i // 2, [1, 3, 8, 20][i % 4],
                              "shared" if i % 3 == 0 else f"g{i}",
                              400 + 400 * (i % 3), 800, i % 2,
                              branch=i % 2, cancelled=(i == 7),
                              revisions=((2, 100),) if i == 5 else (),
                              forecast_return_ticks=8) for i in range(16)]
    result = {p: StressEngine(p, gpu_tokens=1600, cpu_tokens=3200,
                               bandwidth=200).run(sessions)
              for p in ["lru", "ttl", "static", "proposed", "tier_aware", "cost_aware"]}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
