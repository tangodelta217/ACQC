"""Tests for ACQC Demo."""

import math
from pathlib import Path

from acqc_demo.data_gen import generate_demo_dataset, TagSample
from acqc_demo.infer import SoftSensor, create_baseline_model
from acqc_demo.trace import AuditLog


class TestDataGeneration:
    """Tests for data generation module."""
    
    def test_generate_dataset_structure(self):
        """Test that generated dataset has correct structure."""
        dataset = generate_demo_dataset(n_samples=10)
        
        assert "metadata" in dataset
        assert "tags" in dataset
        assert "quality" in dataset
        
        assert dataset["metadata"]["n_samples"] == 10
        assert len(dataset["metadata"]["tags"]) == 4
        assert "hash" in dataset["metadata"]
    
    def test_generate_dataset_tags(self):
        """Test that tags are generated correctly."""
        dataset = generate_demo_dataset(n_samples=5)
        
        for tag_id in ["TI-101", "PI-201", "FI-301", "AI-401"]:
            assert tag_id in dataset["tags"]
            assert len(dataset["tags"][tag_id]) == 5
            
            sample = dataset["tags"][tag_id][0]
            assert "timestamp" in sample
            assert "value" in sample
            assert "qc_flag" in sample
    
    def test_generate_dataset_quality(self):
        """Test that quality variable is generated."""
        dataset = generate_demo_dataset(n_samples=5)
        
        assert len(dataset["quality"]) == 5
        
        sample = dataset["quality"][0]
        assert sample["variable_id"] == "RON"
        assert sample["source"] == "SIMULATED"


class TestInference:
    """Tests for inference module."""
    
    def test_baseline_model_creation(self):
        """Test baseline model configuration."""
        config = create_baseline_model()
        
        assert config.model_id == "soft-sensor-ron-v1"
        assert len(config.input_tags) == 4
        assert config.output_variable == "RON"
    
    def test_soft_sensor_prediction(self):
        """Test soft sensor prediction."""
        sensor = SoftSensor()
        
        tag_values = {
            "TI-101": 350.0,
            "PI-201": 12.5,
            "FI-301": 1500.0,
            "AI-401": 0.85,
        }
        
        pred = sensor.predict(tag_values)
        
        assert pred.variable_id == "RON"
        assert not math.isnan(pred.y_hat)
        assert pred.uncertainty_lower < pred.y_hat < pred.uncertainty_upper
        assert pred.status == "OK"
        assert pred.model_hash == sensor.model_hash
    
    def test_soft_sensor_missing_tags(self):
        """Test soft sensor with missing tags."""
        sensor = SoftSensor()
        
        # Missing AI-401
        tag_values = {
            "TI-101": 350.0,
            "PI-201": 12.5,
            "FI-301": 1500.0,
        }
        
        pred = sensor.predict(tag_values)
        
        assert pred.status == "DEGRADED"
        assert math.isnan(pred.y_hat)
    
    def test_soft_sensor_batch(self):
        """Test batch prediction."""
        dataset = generate_demo_dataset(n_samples=10)
        sensor = SoftSensor()
        
        predictions = sensor.predict_batch(dataset)
        
        assert len(predictions) == 10
        assert all(p.model_id == sensor.config.model_id for p in predictions)


class TestTraceability:
    """Tests for traceability module."""
    
    def test_audit_log_creation(self, tmp_path: Path):
        """Test audit log creation."""
        log = AuditLog(log_dir=tmp_path)
        
        entry = log.log_prediction(
            prediction={"y_hat": 92.5, "timestamp": "2026-01-01T08:00:00Z"},
            input_data={"tags": {"TI-101": 350}},
            model_hash="abc123",
        )
        
        assert entry.event_type == "PREDICTION"
        assert entry.model_hash == "abc123"
        assert len(log.entries) == 1
    
    def test_audit_log_save(self, tmp_path: Path):
        """Test audit log save to file."""
        log = AuditLog(log_dir=tmp_path)
        
        log.log_prediction(
            prediction={"y_hat": 92.5},
            input_data={},
            model_hash="abc123",
        )
        
        path = log.save("test_log.json")
        
        assert path.exists()
        assert path.name == "test_log.json"
    
    def test_audit_log_summary(self, tmp_path: Path):
        """Test audit log summary."""
        log = AuditLog(log_dir=tmp_path)
        
        log.log_prediction({"y_hat": 92.5}, {}, "abc")
        log.log_prediction({"y_hat": 93.0}, {}, "abc")
        log.log_decision(True, "ref", "OP001")
        
        summary = log.summary()
        
        assert summary["PREDICTION"] == 2
        assert summary["DECISION"] == 1


def test_end_to_end():
    """End-to-end test of the demo pipeline."""
    # Generate data
    dataset = generate_demo_dataset(n_samples=20)
    
    # Run inference
    sensor = SoftSensor()
    predictions = sensor.predict_batch(dataset)
    
    # Check results
    assert len(predictions) == 20
    
    # At least some should be OK
    n_ok = sum(1 for p in predictions if p.status == "OK")
    assert n_ok > 0, "Expected at least some OK predictions"
    
    # All should have valid model hash
    assert all(p.model_hash == sensor.model_hash for p in predictions)


if __name__ == "__main__":
    # Run tests with pytest
    import pytest
    pytest.main([__file__, "-v"])
