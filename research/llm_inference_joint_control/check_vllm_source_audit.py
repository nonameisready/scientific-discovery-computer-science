"""Check the pinned vLLM source assumptions without importing vLLM."""
import argparse
import json
from pathlib import Path


def contains(path: Path, needle: str) -> bool:
    return needle in path.read_text(encoding="utf-8")


def audit(root: Path) -> dict:
    scheduler = root / "vllm/v1/core/sched/scheduler.py"
    request = root / "vllm/v1/request.py"
    output = root / "vllm/v1/core/sched/output.py"
    metrics = root / "vllm/v1/spec_decode/metrics.py"
    kv = root / "vllm/v1/core/kv_cache_manager.py"
    required = [scheduler, request, output, metrics, kv]
    missing = [str(p) for p in required if not p.exists()]
    if missing:
        raise FileNotFoundError("missing expected vLLM files: " + ", ".join(missing))
    return {
        "source_root": str(root),
        "commit": __import__("subprocess").check_output(
            ["git", "-C", str(root), "rev-parse", "HEAD"], text=True
        ).strip(),
        "present": {
            "scheduler_schedule": contains(scheduler, "def schedule(self) -> SchedulerOutput"),
            "scheduler_token_budget": contains(scheduler, "token_budget = self.max_num_scheduled_tokens"),
            "scheduler_spec_decode_output": contains(scheduler, "scheduled_spec_decode_tokens"),
            "scheduler_preemption": contains(scheduler, "self._preempt_request(preempted_req"),
            "kv_manager_usage": contains(kv, "def usage(self) -> float"),
            "kv_manager_allocate_lookahead": contains(kv, "num_lookahead_tokens"),
            "request_cached_tokens": contains(request, "self.num_cached_tokens = -1"),
            "global_acceptance_metrics": contains(metrics, "counter_spec_decode_num_accepted_tokens"),
            "scheduler_request_acceptance_field": contains(scheduler, "acceptance_rate"),
            "request_deadline_field": contains(request, "deadline"),
            "request_resident_kv_bytes_field": contains(request, "resident_kv_bytes"),
        },
        "adapter_blockers": [
            "Per-request acceptance_rate is not a scheduler Request field; only aggregate SpecDecodingStats counters are present.",
            "Per-request resident KV bytes are not exposed as a stable Request field; scheduler owns block allocation through KVCacheManager.",
            "A request deadline/SLO debt field is not present in the pinned Request class.",
            "The stock scheduler passes one global num_lookahead_tokens to allocate_slots; per-request RASP budgets require a scheduler patch.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--vllm-root", required=True)
    args = parser.parse_args()
    print(json.dumps(audit(Path(args.vllm_root)), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
