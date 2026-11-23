#!/usr/bin/env python3
"""
lumina/quota_guard.py — Quota Recovery & State Persistence Guard
Reference: DOC-02, DOC-03

Provides safe error handling, exponential backoff, and local checkpointing
to prevent subagent failures during API rate-limit or quota exhaustion events.
"""

import time
import json
import logging
from pathlib import Path
from typing import Callable, Any, Dict, Optional

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

class QuotaGuard:
    """Manages execution retries with exponential backoff and disk checkpoints."""

    def __init__(self, max_retries: int = 4, base_backoff_sec: float = 60.0, checkpoint_dir: str = "data/checkpoints"):
        self.max_retries = max_retries
        self.base_backoff_sec = base_backoff_sec
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def save_checkpoint(self, task_id: str, payload: Dict):
        """Save in-progress task state to disk before backing off."""
        cp_path = self.checkpoint_dir / f"checkpoint_{task_id}.json"
        with open(cp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
        logging.info(f"Task {task_id} checkpoint saved to {cp_path}")

    def load_checkpoint(self, task_id: str) -> Optional[Dict]:
        """Retrieve stored checkpoint if present."""
        cp_path = self.checkpoint_dir / f"checkpoint_{task_id}.json"
        if cp_path.exists():
            with open(cp_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return None

    def clear_checkpoint(self, task_id: str):
        """Remove checkpoint upon successful task completion."""
        cp_path = self.checkpoint_dir / f"checkpoint_{task_id}.json"
        if cp_path.exists():
            cp_path.unlink()

    def execute_with_retry(self, task_id: str, func: Callable[[], Any], fallback_payload: Dict = None) -> Any:
        """Execute a generation call with exponential backoff on 429/quota errors."""
        retries = 0
        while retries <= self.max_retries:
            try:
                result = func()
                self.clear_checkpoint(task_id)
                return result
            except Exception as e:
                err_msg = str(e).lower()
                is_quota = "quota" in err_msg or "429" in err_msg or "rate limit" in err_msg or "resource_exhausted" in err_msg
                if is_quota and retries < self.max_retries:
                    retries += 1
                    sleep_time = self.base_backoff_sec * (2 ** (retries - 1))
                    logging.warning(f"Quota exceeded on task {task_id} (Attempt {retries}/{self.max_retries}). Backing off for {sleep_time:.1f}s. Error: {e}")
                    if fallback_payload:
                        self.save_checkpoint(task_id, fallback_payload)
                    time.sleep(sleep_time)
                else:
                    logging.error(f"Task {task_id} failed permanently after {retries} retries: {e}")
                    raise
