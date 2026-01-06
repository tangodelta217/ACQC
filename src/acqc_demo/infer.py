"""
Inference module for ACQC demo.

Implements a simple soft sensor using linear regression as baseline.
This is a demonstration - not a production model.
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
class Prediction:
    """Single prediction from soft sensor."""
    timestamp: str
    variable_id: str
    y_hat: float
    uncertainty_lower: float
    uncertainty_upper: float
    model_id: str
    model_hash: str
    status: str  # "OK", "DEGRADED", "OOD"


@dataclass
class ModelConfig:
    """Configuration for the soft sensor model."""
    model_id: str
    version: str
    input_tags: list[str]
    output_variable: str
    coefficients: dict[str, float]
    intercept: float
    uncertainty_factor: float  # Multiplier for prediction interval


def create_baseline_model() -> ModelConfig:
    """
    Create a baseline linear model (simulating PLS/PCR).
    
    In production, this would be loaded from a trained artifact.
    """
    return ModelConfig(
        model_id="soft-sensor-ron-v1",
        version="0.1.0-demo",
        input_tags=["TI-101", "PI-201", "FI-301", "AI-401"],
        output_variable="RON",
        coefficients={
            "TI-101": 0.005,
            "PI-201": 0.1,
            "FI-301": 0.0001,
            "AI-401": 2.0,
        },
        intercept=85.0,
        uncertainty_factor=0.5,
    )


def compute_model_hash(config: ModelConfig) -> str:
    """Compute a hash of the model configuration for traceability."""
    config_str = json.dumps(asdict(config), sort_keys=True)
    return hashlib.sha256(config_str.encode()).hexdigest()[:16]


class SoftSensor:
    """Simple soft sensor for demo purposes."""
    
    def __init__(self, config: ModelConfig | None = None):
        self.config = config or create_baseline_model()
        self.model_hash = compute_model_hash(self.config)
        self._ood_threshold = 2.0  # Standard deviations
    
    def predict(
        self,
        tag_values: dict[str, float],
        timestamp: str | None = None,
    ) -> Prediction:
        """
        Make a prediction given current tag values.
        
        Args:
            tag_values: Dict mapping tag_id to current value
            timestamp: ISO timestamp (uses now if not provided)
        
        Returns:
            Prediction with estimate, uncertainty, and status
        """
        ts = timestamp or _utc_now_iso()
        
        # Check for missing or bad inputs
        missing = set(self.config.input_tags) - set(tag_values.keys())
        has_nan = any(
            tag_values.get(t) is None or 
            (isinstance(tag_values.get(t), float) and tag_values.get(t) != tag_values.get(t))
            for t in self.config.input_tags
        )
        
        if missing or has_nan:
            return Prediction(
                timestamp=ts,
                variable_id=self.config.output_variable,
                y_hat=float("nan"),
                uncertainty_lower=float("nan"),
                uncertainty_upper=float("nan"),
                model_id=self.config.model_id,
                model_hash=self.model_hash,
                status="DEGRADED",
            )
        
        # Linear prediction
        y_hat = self.config.intercept
        for tag_id, coef in self.config.coefficients.items():
            y_hat += coef * tag_values.get(tag_id, 0.0)
        
        # Simple uncertainty (in production: from calibration)
        uncertainty = self.config.uncertainty_factor
        
        # OOD check (simplified: based on prediction range)
        status = "OK"
        if y_hat < 80 or y_hat > 100:
            status = "OOD"
            uncertainty *= 2  # Widen interval when OOD
        
        return Prediction(
            timestamp=ts,
            variable_id=self.config.output_variable,
            y_hat=round(y_hat, 3),
            uncertainty_lower=round(y_hat - uncertainty, 3),
            uncertainty_upper=round(y_hat + uncertainty, 3),
            model_id=self.config.model_id,
            model_hash=self.model_hash,
            status=status,
        )
    
    def predict_batch(
        self,
        dataset: dict[str, Any],
    ) -> list[Prediction]:
        """
        Run predictions on a dataset from data_gen.
        
        Args:
            dataset: Output from generate_demo_dataset()
        
        Returns:
            List of predictions
        """
        predictions = []
        n_samples = dataset["metadata"]["n_samples"]
        tags = dataset["tags"]
        
        for i in range(n_samples):
            # Gather tag values for this timestamp
            tag_values = {}
            timestamp = None
            
            for tag_id, samples in tags.items():
                if i < len(samples):
                    sample = samples[i]
                    timestamp = sample["timestamp"]
                    if sample["qc_flag"] == "OK":
                        tag_values[tag_id] = sample["value"]
            
            pred = self.predict(tag_values, timestamp)
            predictions.append(pred)
        
        return predictions


def save_predictions(
    predictions: list[Prediction],
    output_path: Path,
) -> None:
    """Save predictions to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(
            {
                "predictions": [asdict(p) for p in predictions],
                "n_total": len(predictions),
                "n_ok": sum(1 for p in predictions if p.status == "OK"),
                "n_degraded": sum(1 for p in predictions if p.status == "DEGRADED"),
                "n_ood": sum(1 for p in predictions if p.status == "OOD"),
            },
            f,
            indent=2,
        )


if __name__ == "__main__":
    # Quick test
    from acqc_demo.data_gen import generate_demo_dataset
    
    dataset = generate_demo_dataset(n_samples=10)
    sensor = SoftSensor()
    
    print(f"Model: {sensor.config.model_id}")
    print(f"Hash: {sensor.model_hash}")
    
    predictions = sensor.predict_batch(dataset)
    for p in predictions[:3]:
        print(f"  {p.timestamp}: {p.y_hat} [{p.uncertainty_lower}, {p.uncertainty_upper}] ({p.status})")
