"""Send a small fixed trace to an OpenAI-compatible vLLM endpoint.

This records endpoint observations only. It does not label the result as RASP
and does not use future trace rows to make a scheduling decision.
"""
import argparse
import json
import time
import urllib.request


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--base-url', required=True)
    p.add_argument('--trace', required=True)
    p.add_argument('--output', required=True)
    args = p.parse_args()
    with open(args.trace, encoding='utf-8') as f:
        rows = [json.loads(line) for line in f if line.strip()]
    start = time.monotonic()
    with open(args.output, 'w', encoding='utf-8') as out:
        for row in rows:
            target = start + row['arrival_ms'] / 1000
            delay = target - time.monotonic()
            if delay > 0:
                time.sleep(delay)
            body = json.dumps({
                'model': 'Qwen/Qwen2.5-7B-Instruct',
                'messages': [{'role': 'user', 'content': row['prompt']}],
                'max_tokens': row['max_tokens'],
                'temperature': 0
            }).encode()
            req = urllib.request.Request(
                args.base_url.rstrip('/') + '/chat/completions',
                data=body,
                headers={'Content-Type': 'application/json'},
                method='POST')
            t0 = time.monotonic()
            try:
                with urllib.request.urlopen(req, timeout=180) as resp:
                    payload = json.loads(resp.read())
                result = {'evidence_label': 'MEASURED_GPU', 'request_id': row['request_id'],
                          'family': row['family'], 'elapsed_ms': (time.monotonic() - t0) * 1000,
                          'ok': True, 'response': payload}
            except Exception as exc:
                result = {'evidence_label': 'MEASURED_GPU', 'request_id': row['request_id'],
                          'family': row['family'], 'elapsed_ms': (time.monotonic() - t0) * 1000,
                          'ok': False, 'error': type(exc).__name__}
            out.write(json.dumps(result, ensure_ascii=False) + '\n')
            out.flush()


if __name__ == '__main__':
    main()
