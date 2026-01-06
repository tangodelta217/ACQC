"""
ACQC Demo - Entry Point

Run with: python -m acqc_demo
"""

import argparse
import sys
from dataclasses import asdict
from pathlib import Path

from acqc_demo.data_gen import generate_demo_dataset
from acqc_demo.infer import SoftSensor, save_predictions
from acqc_demo.trace import AuditLog


def main() -> int:
    """Main entry point for demo."""
    parser = argparse.ArgumentParser(
        prog="acqc_demo",
        description="ACQC Demo - Minimal runnable skeleton for soft sensor inference",
    )
    parser.add_argument(
        "-n", "--samples",
        type=int,
        default=100,
        help="Number of samples to generate (default: 100)",
    )
    parser.add_argument(
        "-o", "--output",
        type=Path,
        default=Path("./output"),
        help="Output directory (default: ./output)",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output",
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("ACQC Demo - Soft Sensor Inference Skeleton")
    print("=" * 60)
    print()
    
    # Step 1: Generate synthetic data
    print("[1/4] Generating synthetic data...")
    dataset = generate_demo_dataset(
        n_samples=args.samples,
        output_dir=args.output / "data",
    )
    print(f"      Generated {dataset['metadata']['n_samples']} samples")
    print(f"      Tags: {', '.join(dataset['metadata']['tags'])}")
    print(f"      Data hash: {dataset['metadata']['hash']}")
    print()
    
    # Step 2: Initialize soft sensor
    print("[2/4] Initializing soft sensor...")
    sensor = SoftSensor()
    print(f"      Model ID: {sensor.config.model_id}")
    print(f"      Version: {sensor.config.version}")
    print(f"      Model hash: {sensor.model_hash}")
    print()
    
    # Step 3: Run inference
    print("[3/4] Running inference...")
    predictions = sensor.predict_batch(dataset)
    
    n_ok = sum(1 for p in predictions if p.status == "OK")
    n_degraded = sum(1 for p in predictions if p.status == "DEGRADED")
    n_ood = sum(1 for p in predictions if p.status == "OOD")
    
    print(f"      Total predictions: {len(predictions)}")
    print(f"      OK: {n_ok}, DEGRADED: {n_degraded}, OOD: {n_ood}")
    
    # Save predictions
    save_predictions(predictions, args.output / "predictions.json")
    print(f"      Saved to: {args.output / 'predictions.json'}")
    print()
    
    # Step 4: Generate audit log
    print("[4/4] Generating audit log...")
    audit = AuditLog(log_dir=args.output / "audit")
    
    for pred in predictions:
        audit.log_prediction(
            prediction=asdict(pred),
            input_data={"tags": dataset["tags"]},
            model_hash=sensor.model_hash,
        )
        
        if pred.status == "OK":
            audit.log_recommendation(
                recommendation="Continue current operation (within spec)",
                prediction=asdict(pred),
                constraints=["y_hat in [88, 95]"],
                model_hash=sensor.model_hash,
            )
    
    # Simulate one operator decision
    audit.log_decision(
        accepted=True,
        recommendation_ref="DEMO",
        operator_id="DEMO-OPERATOR",
        notes="Demo run - auto-accepted",
    )
    
    log_path = audit.save()
    print(f"      Entries: {audit.summary()}")
    print(f"      Saved to: {log_path}")
    print()
    
    # Summary
    print("=" * 60)
    print("Demo completed successfully!")
    print("=" * 60)
    print()
    print("Output files:")
    print(f"  - {args.output / 'data' / 'dataset.json'}")
    print(f"  - {args.output / 'predictions.json'}")
    print(f"  - {log_path}")
    print()
    
    if args.verbose:
        print("Sample predictions:")
        for p in predictions[:5]:
            print(f"  {p.timestamp}: {p.y_hat:.2f} [{p.uncertainty_lower:.2f}, {p.uncertainty_upper:.2f}] ({p.status})")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
