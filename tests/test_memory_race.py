"""Stop/PreCompact can fire close together as separate processes against one memory.db.

Hermetic: temp files, synthetic transcripts, no network. These tests fail (database is locked, or
overlapping/duplicate archives) without WAL + busy_timeout + the up-front write lock in snapshot()."""

import json
import os
import subprocess
import sys
import threading

from cimcime.memory import Memory


def _line(i: int) -> str:
    return json.dumps({"type": "user", "message": {"role": "user", "content": f"synthetic request number {i}"}}) + "\n"


def _transcript(tmp_path, lines: int = 40):
    t = tmp_path / "t.jsonl"
    t.write_text("".join(_line(i) for i in range(lines)))
    return t


def _ranges(db_path):
    mem = Memory(db_path)
    rows = mem._conn.execute("SELECT start_offset, end_offset FROM archives ORDER BY id").fetchall()
    summaries = mem._conn.execute("SELECT COUNT(*) FROM summaries").fetchone()[0]
    return rows, summaries


def test_database_uses_wal_and_a_busy_timeout(tmp_path):
    mem = Memory(tmp_path / "m.db")
    assert mem._conn.execute("PRAGMA journal_mode").fetchone()[0] == "wal"
    assert mem._conn.execute("PRAGMA busy_timeout").fetchone()[0] >= 10_000


def test_concurrent_threads_archive_the_same_bytes_once(tmp_path):
    db, t = tmp_path / "m.db", _transcript(tmp_path)
    Memory(db)  # create the schema once
    barrier, errors, results = threading.Barrier(8), [], []

    def worker(n: int) -> None:
        try:
            mem = Memory(db)
            barrier.wait()
            trigger = "stop" if n % 2 else "precompact"
            results.append(mem.snapshot("s1", t, trigger, if_due=trigger == "stop", interval=1))
        except Exception as exc:  # noqa: BLE001
            errors.append(repr(exc))

    threads = [threading.Thread(target=worker, args=(n,)) for n in range(8)]
    [th.start() for th in threads]
    [th.join() for th in threads]
    assert errors == []
    ranges, summaries = _ranges(db)
    assert ranges == [(0, t.stat().st_size)]
    assert summaries == 1
    assert sum(1 for r in results if r["snapshot"]) == 1


def test_concurrent_snapshots_of_a_growing_transcript_are_contiguous(tmp_path):
    db, t = tmp_path / "m.db", _transcript(tmp_path, lines=5)
    Memory(db)
    errors, stop = [], threading.Event()

    def appender() -> None:
        i = 100
        while not stop.is_set():
            with t.open("a") as f:
                f.write(_line(i))
            i += 1

    def worker(n: int) -> None:
        try:
            mem = Memory(db)
            for _ in range(15):
                mem.snapshot("s1", t, "stop" if n % 2 else "precompact")
        except Exception as exc:  # noqa: BLE001
            errors.append(repr(exc))

    feeder = threading.Thread(target=appender)
    feeder.start()
    threads = [threading.Thread(target=worker, args=(n,)) for n in range(4)]
    [th.start() for th in threads]
    [th.join() for th in threads]
    stop.set()
    feeder.join()
    assert errors == []
    ranges, _ = _ranges(db)
    assert ranges and ranges[0][0] == 0
    for (_, prev_end), (start, end) in zip(ranges, ranges[1:]):
        assert start == prev_end and end > start


def test_concurrent_hook_processes_do_not_lose_or_duplicate_archives(tmp_path):
    db, t = tmp_path / "m.db", _transcript(tmp_path)
    Memory(db)
    env = {**os.environ, "CIMCIME_MEMORY_DB": str(db)}
    procs = []
    for n in range(6):
        event = "Stop" if n % 2 else "PreCompact"
        payload = json.dumps({"hook_event_name": event, "session_id": "s1", "transcript_path": str(t)})
        p = subprocess.Popen(
            [sys.executable, "-m", "cimcime.cli", "memory-snapshot", "--hook", "--interval", "1"],
            stdin=subprocess.PIPE, stderr=subprocess.PIPE, env=env, text=True,
        )
        p.stdin.write(payload)
        p.stdin.close()
        procs.append(p)
    errs = [p.stderr.read() for p in procs]
    assert [p.wait() for p in procs] == [0] * 6
    assert all("locked" not in e for e in errs), errs
    ranges, _ = _ranges(db)
    assert ranges == [(0, t.stat().st_size)]


def test_a_failed_snapshot_releases_the_write_lock(tmp_path):
    db = tmp_path / "m.db"
    mem = Memory(db)
    try:
        mem.snapshot("s1", tmp_path / "missing.jsonl", "stop")
    except FileNotFoundError:
        pass
    other = Memory(db)
    other._conn.execute("BEGIN IMMEDIATE")  # would block 30 s if the first call leaked its lock
    other._conn.rollback()
