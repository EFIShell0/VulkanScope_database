from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

MAX_RESPONSE_BYTES = 4 * 1024 * 1024
MAX_CHUNK_BYTES = 3 * 1024 * 1024
DEFAULT_API = 'https://vulkanscope-database-api.vulkanscope.workers.dev'
USER_AGENT = 'VulkanScope-Database-preload/1.0.18'


def canonical_bytes(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'), sort_keys=False).encode('utf-8')


def get_json(url: str, attempts: int = 3):
    last = None
    for attempt in range(attempts):
        try:
            req = urllib.request.Request(url, headers={'Accept': 'application/json', 'User-Agent': USER_AGENT})
            with urllib.request.urlopen(req, timeout=25) as response:
                length = int(response.headers.get('Content-Length') or 0)
                if length > MAX_RESPONSE_BYTES:
                    raise RuntimeError(f'response too large: {length} bytes')
                raw = response.read(MAX_RESPONSE_BYTES + 1)
                if len(raw) > MAX_RESPONSE_BYTES:
                    raise RuntimeError('response exceeds 4 MiB')
                if response.status < 200 or response.status >= 300:
                    raise RuntimeError(f'HTTP {response.status}')
            return json.loads(raw.decode('utf-8'))
        except (OSError, UnicodeError, json.JSONDecodeError, urllib.error.URLError, RuntimeError) as exc:
            last = exc
            if attempt + 1 < attempts:
                time.sleep(0.45 * (attempt + 1))
    raise RuntimeError(f'GET failed for {url}: {last}')


def fetch_index(api: str):
    reports = []
    meta = None
    cursor = None
    seen = set()
    while True:
        params = {'limit': '500'}
        if cursor:
            key = (cursor.get('submittedAt'), cursor.get('id'))
            if key in seen:
                raise RuntimeError('API returned a repeated cursor')
            seen.add(key)
            params['beforeSubmittedAt'] = str(key[0])
            params['beforeId'] = str(key[1])
        page = get_json(f"{api}/v1/reports?{urllib.parse.urlencode(params)}")
        if not isinstance(page, dict) or not isinstance(page.get('reports'), list):
            raise RuntimeError('invalid report index response')
        meta = meta or page
        reports.extend(page['reports'])
        cursor = page.get('nextCursor')
        if not cursor:
            break
    ids = [str(item.get('id', '')) for item in reports]
    if len(ids) != len(set(ids)) or any(len(x) != 64 or any(c not in '0123456789abcdef' for c in x) for x in ids):
        raise RuntimeError('report index contains invalid or duplicate ids')
    return meta or {}, reports


def fetch_report(api: str, item: dict):
    rid = item['id']
    payload = get_json(f'{api}/v1/reports/{urllib.parse.quote(rid)}?compact=1')
    if not isinstance(payload, dict) or payload.get('id') != rid:
        raise RuntimeError(f'invalid compact report payload for {rid}')
    return payload


def partition_reports(payloads: list[dict]):
    chunks = []
    current = []
    for payload in payloads:
        candidate = {'schemaVersion': 1, 'reports': current + [payload]}
        size = len(canonical_bytes(candidate))
        if current and size > MAX_CHUNK_BYTES:
            chunks.append(current)
            current = [payload]
            if len(canonical_bytes({'schemaVersion': 1, 'reports': current})) > MAX_CHUNK_BYTES:
                raise RuntimeError(f"single report {payload.get('id')} exceeds preload chunk budget")
        else:
            current.append(payload)
    if current:
        chunks.append(current)
    return chunks


def main():
    parser = argparse.ArgumentParser(description='Build a deploy-time static snapshot from the VulkanScope Database Worker API')
    parser.add_argument('output', help='output data/preload directory')
    parser.add_argument('--api', default=DEFAULT_API)
    parser.add_argument('--workers', type=int, default=8)
    args = parser.parse_args()
    api = args.api.rstrip('/')
    output = Path(args.output).resolve()
    output.mkdir(parents=True, exist_ok=True)
    for old in output.glob('*.json'):
        old.unlink()

    meta, index = fetch_index(api)
    by_id = {item['id']: item for item in index}
    payload_by_id = {}
    workers = max(1, min(16, args.workers))
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as executor:
        futures = {executor.submit(fetch_report, api, item): item['id'] for item in index}
        for future in concurrent.futures.as_completed(futures):
            rid = futures[future]
            payload_by_id[rid] = future.result()

    payloads = [payload_by_id[item['id']] for item in index]
    chunk_meta = []
    for reports in partition_reports(payloads):
        body = canonical_bytes({'schemaVersion': 1, 'reports': reports})
        digest = hashlib.sha256(body).hexdigest()
        name = f'reports.{digest[:16]}.json'
        (output / name).write_bytes(body)
        chunk_meta.append({'file': name, 'sha256': digest, 'byteLength': len(body), 'reportCount': len(reports)})

    generated = dt.datetime.now(dt.timezone.utc).isoformat().replace('+00:00', 'Z')
    manifest = {
        'schemaVersion': 1,
        'databaseVersion': '1.0.18',
        'sourceSchemaVersion': meta.get('schemaVersion'),
        'normalizerVersion': meta.get('normalizerVersion', 16),
        'publishedVulkanSpec': meta.get('publishedVulkanSpec', 'Vulkan 1.4.362 (2026-09-04)'),
        'vulkanRegistryBaseline': meta.get('vulkanRegistryBaseline', 'VulkanScope producer/query baseline 1.4.362'),
        'producerQueryBaseline': 'VulkanScope 1.0.19 · Vulkan 1.4.362',
        'compatibleProducer': meta.get('compatibleProducer', 'VulkanScope 1.0.19+ · schema 2 / technical report 3'),
        'generatedAt': generated,
        'reportCount': len(index),
        'reports': index,
        'chunks': chunk_meta,
    }
    (output / 'manifest.json').write_bytes(canonical_bytes(manifest))
    print(f'Built preload snapshot: reports={len(index)} chunks={len(chunk_meta)} output={output}')


if __name__ == '__main__':
    main()
