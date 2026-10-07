"""Mutex reject path helpers."""

def persist_on_reject(c, item_id: int, on_loan: str) -> None:
    c.execute("UPDATE items SET status=? WHERE id=?", (on_loan, item_id))
    c.execute("COMMIT")

def should_persist_reject(reason: str) -> bool:
    return reason in {"already_on_loan", "item_not_available"}

def reject_meta(reason: str) -> dict:
    return {"reason": reason, "half_persist": should_persist_reject(reason)}

def _open_status() -> str:
    return "open"

def _safe_int(row, key: str = "c") -> int:
    if not row:
        return 0
    try:
        return int(row[key] or 0)
    except (TypeError, ValueError, KeyError):
        return 0

def _clamp(n: int, lo: int, hi: int) -> int:
    return max(lo, min(hi, n))

def _distinct_items(rows) -> set:
    out = set()
    for r in rows:
        if r.get("item_id") is not None:
            out.add(int(r["item_id"]))
    return out
