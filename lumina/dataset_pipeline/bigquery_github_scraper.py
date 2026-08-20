"""
Lumina PLC-LLM-OS: Google BigQuery GitHub Scraper v2
=====================================================
Uses google-cloud-bigquery with google.api_core REST transport (no pandas/db-dtypes).
This bypasses the Python 3.13 Cython ABI crash that affects all pandas 2.x builds.

HOW TO RUN:
  $env:GOOGLE_APPLICATION_CREDENTIALS = "C:\path\to\gcp_service_key.json.json"
  python bigquery_github_scraper.py
"""

import os
import re
import json
import time
import logging
import hashlib
from pathlib import Path
from google.oauth2 import service_account
from google.auth.transport.requests import Request as GoogleRequest
import urllib.request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("BigQueryScraper_v2")

# ── Config ────────────────────────────────────────────────────────────────────
BASE_DIR     = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
OUTPUT_DIR   = BASE_DIR / "data"
CLEAN_OUTPUT = OUTPUT_DIR / "bigquery_github_verified.jsonl"
KEY_FILE     = os.environ.get(
    "GOOGLE_APPLICATION_CREDENTIALS",
    r"C:\Users\majip\Downloads\LLM REASEARCH\gcp_service_key.json.json"
)
PROJECT_ID   = "spry-reference-473322-j1"

MIN_CODE = 150
MAX_CODE = 40_000

# ── SQL ───────────────────────────────────────────────────────────────────────
BIGQUERY_SQL = """
SELECT
  f.repo_name,
  f.path,
  c.content
FROM
  `bigquery-public-data.github_repos.files` AS f
JOIN
  `bigquery-public-data.github_repos.contents` AS c
  ON f.id = c.id
WHERE (
    LOWER(f.path) LIKE '%.st'
    OR LOWER(f.path) LIKE '%.scl'
    OR LOWER(f.path) LIKE '%.tcpou'
    OR LOWER(f.path) LIKE '%.tcdut'
    OR LOWER(f.path) LIKE '%.tcgvl'
)
AND c.content IS NOT NULL
AND c.binary = false
LIMIT 30000
"""

# ── XML Stripper ──────────────────────────────────────────────────────────────
_CDATA_DECL  = re.compile(r"<Declaration>\s*<!\[CDATA\[(.*?)]]>\s*</Declaration>", re.DOTALL)
_CDATA_IMPL  = re.compile(r"<ST>\s*<!\[CDATA\[(.*?)]]>\s*</ST>", re.DOTALL)
_CDATA_GEN   = re.compile(r"<!\[CDATA\[(.*?)]]>", re.DOTALL)
_XML_STRIP   = re.compile(r"<[^>]+>")

def strip_xml(raw: str, ext: str) -> str:
    if ext in (".tcpou", ".tcdut", ".tcgvl"):
        decl = _CDATA_DECL.search(raw)
        impl = _CDATA_IMPL.search(raw)
        if decl and impl:
            return f"{decl.group(1).strip()}\n{impl.group(1).strip()}\nEND_FUNCTION_BLOCK"
        hits = _CDATA_GEN.findall(raw)
        if hits:
            return "\n\n".join(h.strip() for h in hits if len(h.strip()) > 30)
    return raw.strip()

# ── Linter ────────────────────────────────────────────────────────────────────
_BLK_START = re.compile(r"^\s*(PROGRAM|FUNCTION_BLOCK|FUNCTION|ACTION)\s+\w+", re.I|re.M)
_BLK_END   = re.compile(r"(END_PROGRAM|END_FUNCTION_BLOCK|END_FUNCTION|END_ACTION)", re.I)
_VAR_OPEN  = re.compile(r"\bVAR\b", re.I)
_VAR_CLOSE = re.compile(r"\bEND_VAR\b", re.I)
_IF_OPEN   = re.compile(r"\bIF\b", re.I)
_IF_CLOSE  = re.compile(r"\bEND_IF\b", re.I)
_ASSIGN    = re.compile(r":=")

def lint(code: str, ext: str) -> tuple:
    if len(code) < MIN_CODE: return False, "Too short"
    if len(code) > MAX_CODE: return False, "Too long"
    if ext in (".st", ".scl"):
        if not _BLK_START.search(code): return False, "No block declaration"
        if not _BLK_END.search(code):   return False, "Block never closed"
    if ext in (".tcpou", ".tcdut", ".tcgvl"):
        if not (_ASSIGN.search(code) or _IF_OPEN.search(code) or _VAR_OPEN.search(code)):
            return False, "No ST logic signals"
    n_if  = len(_IF_OPEN.findall(code))
    n_end = len(_IF_CLOSE.findall(code))
    if n_if > 3 and abs(n_if - n_end) > 3: return False, "Unbalanced IF/END_IF"
    return True, "PASS"

# ── REST BigQuery client (no pandas) ─────────────────────────────────────────
def run_query_via_rest(sql: str, project: str, credentials) -> list:
    """
    Fires a BigQuery jobs.query REST call and polls for results.
    Returns list of row dicts. No pandas, no db-dtypes, no Cython crashes.
    """
    ENDPOINT = f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}/jobs"

    # Refresh credentials to get access token
    credentials.refresh(GoogleRequest())
    token = credentials.token

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type":  "application/json"
    }

    # Step 1 — submit the job
    body = json.dumps({
        "configuration": {
            "query": {
                "query":            sql,
                "useLegacySql":     False,
                "location":         "US",
                "useQueryCache":    True,
                "allowLargeResults": True,
                "createDisposition": "CREATE_IF_NEEDED",
                "writeDisposition":  "WRITE_TRUNCATE"
            }
        }
    }).encode()

    logger.info("Step 1/4 — Submitting BigQuery job to Google Cloud...")
    req  = urllib.request.Request(ENDPOINT, data=body, headers=headers, method="POST")
    with urllib.request.urlopen(req) as resp:
        job_info = json.loads(resp.read())

    job_id = job_info["jobReference"]["jobId"]
    logger.info(f"Step 2/4 — Job submitted. ID: {job_id}")
    logger.info("Step 2/4 — Google is scanning the GitHub mirror (~200GB). Waiting for results...")

    # Step 2 — poll until complete
    status_url = f"{ENDPOINT}/{job_id}?location=US"
    start = time.time()
    while True:
        req2 = urllib.request.Request(status_url, headers=headers)
        with urllib.request.urlopen(req2) as r2:
            status = json.loads(r2.read())
        state = status["status"]["state"]
        elapsed = int(time.time() - start)
        logger.info(f"  Query state: {state} (elapsed: {elapsed}s)")
        if state == "DONE":
            if "errorResult" in status["status"]:
                raise RuntimeError(f"BigQuery error: {status['status']['errorResult']}")
            break
        time.sleep(5)

    # Step 3 — paginate through results
    logger.info("Step 3/4 — Downloading rows from BigQuery...")
    rows_url = (
        f"https://bigquery.googleapis.com/bigquery/v2/projects/{project}"
        f"/queries/{job_id}?location=US&maxResults=10000"
    )
    all_rows = []
    page_token = None
    page = 0
    while True:
        url = rows_url + (f"&pageToken={page_token}" if page_token else "")
        req3 = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req3) as r3:
            result = json.loads(r3.read())
        schema_fields = [f["name"] for f in result.get("schema", {}).get("fields", [])]
        raw_rows = result.get("rows", [])
        for raw in raw_rows:
            row = {schema_fields[i]: v.get("v") for i, v in enumerate(raw["f"])}
            all_rows.append(row)
        page += 1
        page_token = result.get("pageToken")
        logger.info(f"  Page {page}: got {len(raw_rows)} rows (total so far: {len(all_rows)})")
        if not page_token:
            break
        # Refresh token if needed
        credentials.refresh(GoogleRequest())
        headers["Authorization"] = f"Bearer {credentials.token}"

    return all_rows

# ── Main ──────────────────────────────────────────────────────────────────────
def run():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info("=" * 65)
    logger.info("  LUMINA BigQuery GitHub Scraper v2 (pandas-free REST mode)")
    logger.info("=" * 65)
    logger.info(f"  Project  : {PROJECT_ID}")
    logger.info(f"  Key file : {KEY_FILE}")
    logger.info(f"  Output   : {CLEAN_OUTPUT}")
    logger.info(f"  SQL LIMIT: 30,000 rows  |  Cost: ~$0.00 (free tier)")
    logger.info("=" * 65)

    # Load existing hashes for deduplication
    seen = set()
    if CLEAN_OUTPUT.exists():
        with open(CLEAN_OUTPUT, "r", encoding="utf-8") as f:
            for line in f:
                try: seen.add(json.loads(line).get("id", ""))
                except: pass
    logger.info(f"  Loaded {len(seen)} existing hashes for deduplication.")

    # Authenticate
    creds = service_account.Credentials.from_service_account_file(
        KEY_FILE,
        scopes=["https://www.googleapis.com/auth/bigquery",
                "https://www.googleapis.com/auth/cloud-platform"]
    )
    logger.info("  Authentication: OK (Service Account)")

    # Execute query
    rows = run_query_via_rest(BIGQUERY_SQL, PROJECT_ID, creds)
    logger.info(f"Step 4/4 — Processing {len(rows):,} rows through the verification pipeline...")

    stats = {"total": len(rows), "passed": 0, "failed": 0, "dupes": 0}
    lang_map = {
        ".scl": "Siemens SCL", ".st": "IEC 61131-3 Structured Text",
        ".tcpou": "Beckhoff TwinCAT 3 ST", ".tcdut": "TwinCAT Data Unit Type",
        ".tcgvl": "TwinCAT Global Variable List"
    }

    with open(CLEAN_OUTPUT, "a", encoding="utf-8") as out_f:
        for i, row in enumerate(rows):
            repo    = row.get("repo_name", "")
            path    = row.get("path", "")
            content = row.get("content") or ""
            ext     = Path(path).suffix.lower()

            code = strip_xml(content, ext)
            ok, reason = lint(code, ext)
            if not ok:
                stats["failed"] += 1
                continue

            h = hashlib.md5(code.encode()).hexdigest()
            if h in seen:
                stats["dupes"] += 1
                continue
            seen.add(h)

            lang   = lang_map.get(ext, "IEC 61131-3 Structured Text")
            name   = Path(path).stem
            record = {
                "id":     h,
                "source": f"bigquery/github/{repo}",
                "messages": [
                    {"role": "user",      "content": f"Write a complete {lang} implementation for a module called '{name}'."},
                    {"role": "assistant", "content": code}
                ]
            }
            out_f.write(json.dumps(record) + "\n")
            out_f.flush()
            stats["passed"] += 1

            if i % 500 == 0 and i > 0:
                logger.info(f"  Progress: {i:,}/{stats['total']:,} processed | "
                            f"passed={stats['passed']} | failed={stats['failed']}")

    logger.info("=" * 65)
    logger.info("  BIGQUERY SCRAPER COMPLETE")
    logger.info("=" * 65)
    logger.info(f"  Total rows from BigQuery : {stats['total']:>10,}")
    logger.info(f"  Linter PASS (verified)   : {stats['passed']:>10,}")
    logger.info(f"  Linter FAIL (discarded)  : {stats['failed']:>10,}")
    logger.info(f"  Duplicates skipped       : {stats['dupes']:>10,}")
    logger.info(f"  Output file              : {CLEAN_OUTPUT}")

if __name__ == "__main__":
    run()
