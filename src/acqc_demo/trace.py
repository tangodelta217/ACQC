"""
Traceability module for ACQC demo.

Provides minimal audit logging for predictions and decisions.
"""

import json
import hashlib
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass
class TraceEntry:
    """Single audit log entry."""
    entry_id: str
    timestamp: str
    event_type: str  # "PREDICTION", "RECOMMENDATION", "DECISION", "ERROR"
    payload: dict[str, Any]
    data_hash: str
    model_hash: str | None
    operator_id: str | None


class AuditLog:
    """Simple audit log for demo traceability."""
    
    def __init__(self, log_dir: Path | None = None):
        self.log_dir = log_dir or Path("./output/audit")
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.entries: list[TraceEntry] = []
        self._counter = 0
    
    def _generate_id(self) -> str:
        """Generate unique entry ID."""
        self._counter += 1
        ts = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S")
        return f"TRACE-{ts}-{self._counter:04d}"
    
    def _compute_hash(self, data: Any) -> str:
        """Compute hash of data for integrity."""
        return hashlib.sha256(
            json.dumps(data, sort_keys=True, default=str).encode()
        ).hexdigest()[:16]
    
    def log_prediction(
        self,
        prediction: dict[str, Any],
        input_data: dict[str, Any],
        model_hash: str,
    ) -> TraceEntry:
        """Log a prediction event."""
        entry = TraceEntry(
            entry_id=self._generate_id(),
            timestamp=_utc_now_iso(),
            event_type="PREDICTION",
            payload={
                "prediction": prediction,
                "input_summary": {
                    "n_tags": len(input_data.get("tags", {})),
                    "timestamp": prediction.get("timestamp"),
                },
            },
            data_hash=self._compute_hash(input_data),
            model_hash=model_hash,
            operator_id=None,
        )
        self.entries.append(entry)
        return entry
    
    def log_recommendation(
        self,
        recommendation: str,
        prediction: dict[str, Any],
        constraints: list[str],
        model_hash: str,
    ) -> TraceEntry:
        """Log a recommendation event."""
        entry = TraceEntry(
            entry_id=self._generate_id(),
            timestamp=_utc_now_iso(),
            event_type="RECOMMENDATION",
            payload={
                "recommendation": recommendation,
                "prediction_ref": prediction.get("timestamp"),
                "constraints_applied": constraints,
                "status": prediction.get("status"),
            },
            data_hash=self._compute_hash(prediction),
            model_hash=model_hash,
            operator_id=None,
        )
        self.entries.append(entry)
        return entry
    
    def log_decision(
        self,
        accepted: bool,
        recommendation_ref: str,
        operator_id: str,
        notes: str | None = None,
    ) -> TraceEntry:
        """Log an operator decision."""
        entry = TraceEntry(
            entry_id=self._generate_id(),
            timestamp=_utc_now_iso(),
            event_type="DECISION",
            payload={
                "accepted": accepted,
                "recommendation_ref": recommendation_ref,
                "notes": notes,
            },
            data_hash=self._compute_hash({"accepted": accepted, "ref": recommendation_ref}),
            model_hash=None,
            operator_id=operator_id,
        )
        self.entries.append(entry)
        return entry
    
    def log_error(
        self,
        error_type: str,
        message: str,
        context: dict[str, Any] | None = None,
    ) -> TraceEntry:
        """Log an error event."""
        entry = TraceEntry(
            entry_id=self._generate_id(),
            timestamp=_utc_now_iso(),
            event_type="ERROR",
            payload={
                "error_type": error_type,
                "message": message,
                "context": context or {},
            },
            data_hash=self._compute_hash({"error": error_type, "msg": message}),
            model_hash=None,
            operator_id=None,
        )
        self.entries.append(entry)
        return entry
    
    def save(self, filename: str = "audit_log.json") -> Path:
        """Save audit log to file."""
        output_path = self.log_dir / filename
        
        with open(output_path, "w") as f:
            json.dump(
                {
                    "log_version": "1.0",
                    "generated_at": _utc_now_iso(),
                    "n_entries": len(self.entries),
                    "entries": [asdict(e) for e in self.entries],
                },
                f,
                indent=2,
            )
        
        return output_path
    
    def summary(self) -> dict[str, int]:
        """Get summary of log entries by type."""
        counts = {"PREDICTION": 0, "RECOMMENDATION": 0, "DECISION": 0, "ERROR": 0}
        for entry in self.entries:
            counts[entry.event_type] = counts.get(entry.event_type, 0) + 1
        return counts


if __name__ == "__main__":
    # Quick test
    log = AuditLog()
    
    log.log_prediction(
        prediction={"y_hat": 92.5, "timestamp": "2026-01-01T08:00:00Z"},
        input_data={"tags": {"TI-101": 350}},
        model_hash="abc123",
    )
    
    log.log_recommendation(
        recommendation="Increase feed rate by 2%",
        prediction={"y_hat": 92.5, "timestamp": "2026-01-01T08:00:00Z", "status": "OK"},
        constraints=["max_rate < 1600"],
        model_hash="abc123",
    )
    
    log.log_decision(
        accepted=True,
        recommendation_ref="TRACE-...",
        operator_id="OP001",
        notes="Verified with shift supervisor",
    )
    
    path = log.save()
    print(f"Saved audit log to: {path}")
    print(f"Summary: {log.summary()}")
