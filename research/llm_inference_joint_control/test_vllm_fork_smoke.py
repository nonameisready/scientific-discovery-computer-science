"""CPU-only smoke tests for the pinned vLLM scheduler fork.

These tests do not import vLLM or allocate a model. They compile the patched
source and execute the small RASP policy hook extracted from that source, so a
missing GPU/runtime dependency cannot hide a scheduler wiring regression.
"""
import ast
import os
import unittest
from pathlib import Path
from types import SimpleNamespace


VLLM_ROOT = os.environ.get("VLLM_ROOT", "/private/tmp/vllm-ramp-v0.13.0")
SCHEDULER = os.path.join(
    VLLM_ROOT, "vllm", "v1", "core", "sched", "scheduler.py"
)
SCHEDULER_PATH = Path(SCHEDULER)


def load_rasp_hook():
    source = SCHEDULER_PATH.read_text(encoding="utf-8")
    tree = ast.parse(source, filename=SCHEDULER)
    scheduler_class = next(
        node for node in tree.body
        if isinstance(node, ast.ClassDef) and node.name == "Scheduler"
    )
    method = next(
        node for node in scheduler_class.body
        if isinstance(node, ast.FunctionDef)
        and node.name == "_rasp_lookahead_tokens"
    )
    namespace = {"Request": object}
    exec(compile(ast.Module(body=[method], type_ignores=[]), SCHEDULER, "exec"), namespace)
    return namespace[method.name], source


class VllmForkSmokeTests(unittest.TestCase):
    def test_scheduler_source_compiles_and_has_two_rasp_allocation_sites(self):
        source = SCHEDULER_PATH.read_text(encoding="utf-8")
        compile(source, SCHEDULER, "exec")
        self.assertEqual(source.count("self._rasp_lookahead_tokens(request)"), 2)

    def test_hook_clamps_and_preserves_stock_behavior(self):
        hook, _ = load_rasp_hook()
        stock = SimpleNamespace(num_lookahead_tokens=5, num_spec_tokens=5,
                                use_eagle=True)
        self.assertEqual(hook(stock, SimpleNamespace()), 5)
        self.assertEqual(hook(stock, SimpleNamespace(rasp_speculative_tokens=99)), 5)
        self.assertEqual(hook(stock, SimpleNamespace(rasp_speculative_tokens=-2)), 0)

        no_eagle = SimpleNamespace(num_lookahead_tokens=5, num_spec_tokens=5,
                                   use_eagle=False)
        self.assertEqual(
            hook(no_eagle, SimpleNamespace(rasp_speculative_tokens=3)), 0
        )


if __name__ == "__main__":
    unittest.main()
