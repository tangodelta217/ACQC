"""
Data generation module for ACQC demo.

Generates synthetic time series simulating:
- OT process tags (temperature, pressure, flow)
- PAT spectral features (simulated)
- Quality variable (target for soft sensor)
"""

import json
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterator
import hashlib
import random
import math


@dataclass
class TagSample:
    """Single sample of process data."""
    timestamp: str
    tag_id: str
    value: float
    unit: str
    qc_flag: str  # "OK", "SUSPECT", "BAD"


@dataclass
class QualitySample:
    """Simulated quality variable (ground truth)."""
    timestamp: str
    variable_id: str
    value: float
    unit: str
    source: str  # "LAB" or "SIMULATED"


def generate_tag_series(
    tag_id: str,
    base_value: float,
    noise_std: float,
    unit: str,
    n_samples: int = 100,
    interval_seconds: int = 60,
    start_time: datetime | None = None,
) -> Iterator[TagSample]:
    """Generate a synthetic time series for a process tag."""
    start = start_time or datetime.utcnow()
    
    for i in range(n_samples):
        ts = start + timedelta(seconds=i * interval_seconds)
        # Add trend + noise + occasional drift
        trend = 0.001 * i * base_value
        noise = random.gauss(0, noise_std)
        drift = 0.1 * base_value * math.sin(2 * math.pi * i / 50)
        
        value = base_value + trend + noise + drift
        
        # Simulate QC flags
        qc = "OK"
        if random.random() < 0.02:
            qc = "SUSPECT"
        if random.random() < 0.005:
            qc = "BAD"
            value = float("nan")
        
        yield TagSample(
            timestamp=ts.isoformat() + "Z",
            tag_id=tag_id,
            value=round(value, 4),
            unit=unit,
            qc_flag=qc,
        )


def generate_quality_variable(
    tag_samples: list[list[TagSample]],
    variable_id: str = "RON",
    unit: str = "octane",
) -> Iterator[QualitySample]:
    """
    Generate a simulated quality variable based on input tags.
    
    This simulates what a soft sensor would predict, but here we use it
    as "ground truth" for demo purposes.
    """
    # Assume all tag lists have same timestamps
    if not tag_samples or not tag_samples[0]:
        return
    
    n = len(tag_samples[0])
    for i in range(n):
        # Simple linear combination with noise (simulating real relationship)
        base = 90.0
        for tag_list in tag_samples:
            if i < len(tag_list) and not math.isnan(tag_list[i].value):
                # Normalize contribution
                base += 0.01 * tag_list[i].value
        
        # Add measurement noise (lab uncertainty)
        lab_noise = random.gauss(0, 0.3)
        value = base + lab_noise
        
        yield QualitySample(
            timestamp=tag_samples[0][i].timestamp,
            variable_id=variable_id,
            value=round(value, 2),
            unit=unit,
            source="SIMULATED",
        )


def generate_demo_dataset(
    n_samples: int = 100,
    output_dir: Path | None = None,
) -> dict:
    """
    Generate a complete demo dataset.
    
    Returns dict with tags and quality data, optionally saves to files.
    """
    start_time = datetime(2026, 1, 1, 8, 0, 0)
    
    # Define process tags (simulated)
    tag_configs = [
        ("TI-101", 350.0, 5.0, "°C"),      # Temperature
        ("PI-201", 12.5, 0.3, "bar"),       # Pressure  
        ("FI-301", 1500.0, 50.0, "kg/h"),   # Flow
        ("AI-401", 0.85, 0.02, "ratio"),    # Analyzer (simulated PAT)
    ]
    
    all_tags = {}
    tag_lists = []
    
    for tag_id, base, noise, unit in tag_configs:
        samples = list(generate_tag_series(
            tag_id=tag_id,
            base_value=base,
            noise_std=noise,
            unit=unit,
            n_samples=n_samples,
            interval_seconds=60,
            start_time=start_time,
        ))
        all_tags[tag_id] = samples
        tag_lists.append(samples)
    
    # Generate quality variable
    quality_samples = list(generate_quality_variable(
        tag_samples=tag_lists,
        variable_id="RON",
        unit="octane",
    ))
    
    dataset = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "n_samples": n_samples,
            "tags": [t[0] for t in tag_configs],
            "quality_variable": "RON",
            "hash": hashlib.sha256(
                json.dumps([asdict(s) for s in quality_samples]).encode()
            ).hexdigest()[:16],
        },
        "tags": {k: [asdict(s) for s in v] for k, v in all_tags.items()},
        "quality": [asdict(s) for s in quality_samples],
    }
    
    if output_dir:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        with open(output_dir / "dataset.json", "w") as f:
            json.dump(dataset, f, indent=2)
    
    return dataset


if __name__ == "__main__":
    # Quick test
    dataset = generate_demo_dataset(n_samples=10)
    print(f"Generated {dataset['metadata']['n_samples']} samples")
    print(f"Tags: {dataset['metadata']['tags']}")
    print(f"Hash: {dataset['metadata']['hash']}")
