from models.analysis_run import AnalysisRun
from models.horner_correction import HornerCorrection
from models.temperature_measurement import TemperatureMeasurement
import pytest
import numpy as np


def test_calculate_horner_ratio():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    result = correction.calculate_horner_ratio(1)

    assert result == 4


def test_calculate_log_horner_ratio():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    result = correction.calculate_log_horner_ratio(1)

    assert result == pytest.approx(np.log(4))

def create_test_run():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    shut_in_times = [1, 2, 3, 4, 5]

    for i, time in enumerate(shut_in_times):
        temperature = 100 - 10 * np.log((3 + time) / time)

        measurement = TemperatureMeasurement(
            measurement_id=i + 1,
            borehole_id="BH1",
            depth=3000,
            temperature=temperature,
            measurement_time=None,
            time_since_circulation=time
        )

        run.add_measurements(measurement)

    return run

def test_perform_regression():
    run = create_test_run()
    correction = HornerCorrection(run)

    slope, intercept = correction.perform_regression()

    assert slope == pytest.approx(-10)
    assert intercept == pytest.approx(100)

@pytest.mark.parametrize("shut_in_time", [0, -1, -5])
def test_invalid_shut_in_time(shut_in_time):
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    with pytest.raises(ValueError):
        correction.calculate_horner_ratio(shut_in_time)

def test_insufficient_measurements():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    with pytest.raises(ValueError, match="Insufficient values"):
        correction.perform_regression()

@pytest.mark.parametrize("shut_in_time", [0, -1, -5])
def test_invalid_shut_in_time(shut_in_time):
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    with pytest.raises(ValueError):
        correction.calculate_horner_ratio(shut_in_time)

def test_insufficient_measurements():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    with pytest.raises(ValueError, match="Insufficient values"):
        correction.perform_regression()

@pytest.mark.parametrize("circulation_time", [0, -1, -5])
def test_invalid_circulation_time(circulation_time):
    with pytest.raises(ValueError, match="Circulation time"):
        AnalysisRun("RUN1", "BH1", 3000, circulation_time)

def test_repeated_shut_in_times():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    for i in range(3):
        measurement = TemperatureMeasurement(
            measurement_id=i + 1,
            borehole_id="BH1",
            depth=3000,
            temperature=90 + i,
            measurement_time=None,
            time_since_circulation=2
        )
        run.add_measurements(measurement)

    correction = HornerCorrection(run)

    with pytest.raises(ValueError, match="distinct Horner values"):
        correction.perform_regression()

def test_calculate_static_formation_temperature():
    run = create_test_run()
    correction = HornerCorrection(run)

    temperature = correction.calculate_static_formation_temperature()

    assert temperature == pytest.approx(100, abs=0.01)

def test_perform_regression():
    run = create_test_run()
    correction = HornerCorrection(run)

    slope, intercept = correction.perform_regression()

    assert slope == pytest.approx(-10, abs=0.01)
    assert intercept == pytest.approx(100, abs=0.01)

def test_prepare_regression_data():
    run = create_test_run()
    correction = HornerCorrection(run)

    x_values, y_values = correction.prepare_regression_data()

    assert len(x_values) == 5
    assert len(y_values) == 5

    assert x_values[0] == pytest.approx(np.log(4))
    assert y_values[0] == pytest.approx(
        100 - 10 * np.log(4)
    )

def test_regression_handles_noisy_measurements():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    shut_in_times = [1, 2, 3, 4, 5]
    noise = [0.2, -0.1, 0.15, -0.2, 0.1]

    for i, time in enumerate(shut_in_times):
        temperature = (
            100
            - 10 * np.log((3 + time) / time)
            + noise[i]
        )

        measurement = TemperatureMeasurement(
            measurement_id=i + 1,
            borehole_id="BH1",
            depth=3000,
            temperature=temperature,
            measurement_time=None,
            time_since_circulation=time
        )

        run.add_measurements(measurement)

    engine = HornerCorrection(run)

    slope, intercept = engine.perform_regression()

    assert slope == pytest.approx(-10, abs=0.2)
    assert intercept == pytest.approx(100, abs=0.2)

def test_regression_recovers_known_values():
    run = create_test_run()
    engine = HornerCorrection(run)

    slope, intercept = engine.perform_regression()

    assert slope == pytest.approx(-10, abs=1e-10)
    assert intercept == pytest.approx(100, abs=1e-10)

def test_regression_rejects_nearly_identical_horner_values():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    shut_in_times = [1, 1.000000000001, 1.000000000002]

    for i, time in enumerate(shut_in_times):
        temperature = 100 - 10 * np.log((3 + time) / time)

        measurement = TemperatureMeasurement(
            measurement_id=i + 1,
            borehole_id="BH1",
            depth=3000,
            temperature=temperature,
            measurement_time=None,
            time_since_circulation=time
        )

        run.add_measurements(measurement)

    engine = HornerCorrection(run)

    with pytest.raises(ValueError, match="too close"):
        engine.perform_regression()

def test_invalid_circulation_time_in_log_ratio():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    run.circulation_time = 0

    with pytest.raises(ValueError, match="Circulation time"):
        correction.calculate_log_horner_ratio(2)

def test_zero_temperature_is_valid():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=3000,
        temperature=0,
        measurement_time=None,
        time_since_circulation=2
    )

    run.add_measurements(measurement)

    assert run.measurements[0].temperature == 0

def test_negative_temperature_is_valid():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=3000,
        temperature=-5,
        measurement_time=None,
        time_since_circulation=2
    )

    run.add_measurements(measurement)

    assert run.measurements[0].temperature == -5

def test_regression_data_preserves_measurement_order():
    run = create_test_run()
    correction = HornerCorrection(run)

    x_values, y_values = correction.prepare_regression_data()

    for i, measurement in enumerate(run.measurements):
        expected_x = np.log(
            (3 + measurement.time_since_circulation)
            / measurement.time_since_circulation
        )

        assert x_values[i] == pytest.approx(expected_x)
        assert y_values[i] == pytest.approx(measurement.temperature)

def test_very_small_shut_in_time():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    result = correction.calculate_log_horner_ratio(0.000001)

    expected = np.log((3 + 0.000001) / 0.000001)

    assert result == pytest.approx(expected)
    assert np.isfinite(result)

def test_very_large_shut_in_time():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)
    correction = HornerCorrection(run)

    result = correction.calculate_log_horner_ratio(1e12)

    assert result == pytest.approx(0, abs=1e-10)
    assert np.isfinite(result)

def test_nan_temperature_is_rejected():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=3000,
        temperature=float("nan"),
        measurement_time=None,
        time_since_circulation=2
    )

    with pytest.raises(ValueError):
        run.add_measurements(measurement)

@pytest.mark.parametrize("temperature", [float("inf"), float("-inf")])
def test_infinite_temperature_is_rejected(temperature):
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=3000,
        temperature=temperature,
        measurement_time=None,
        time_since_circulation=2
    )

    with pytest.raises(ValueError, match="finite"):
        run.add_measurements(measurement)

@pytest.mark.parametrize(
    "uncertainty",
    [-1, float("nan"), float("inf"), float("-inf")]
)
def test_invalid_measurement_uncertainty_is_rejected(uncertainty):
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=3000,
        temperature=100,
        measurement_time=None,
        time_since_circulation=2,
        measurement_uncertainty=uncertainty
    )

    with pytest.raises(ValueError):
        run.add_measurements(measurement)

@pytest.mark.parametrize("depth", [0, -100])
def test_invalid_depth_is_rejected(depth):
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=depth,
        temperature=100,
        measurement_time=None,
        time_since_circulation=2
    )

    with pytest.raises(ValueError, match="Depth must be positive"):
        run.add_measurements(measurement)

def test_invalid_borehole_id_is_rejected():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH2",
        depth=3000,
        temperature=100,
        measurement_time=None,
        time_since_circulation=2
    )

    with pytest.raises(ValueError, match="another borehole"):
        run.add_measurements(measurement)

def test_measurement_at_different_analysis_depth_is_rejected():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=3500,
        temperature=100,
        measurement_time=None,
        time_since_circulation=2
    )

    with pytest.raises(ValueError, match="another depth"):
        run.add_measurements(measurement)

def test_duplicate_measurement_ids_are_rejected():
    run = create_test_run()

    measurement = TemperatureMeasurement(
        measurement_id=1,
        borehole_id="BH1",
        depth=3000,
        temperature=100,
        measurement_time=None,
        time_since_circulation=6
    )

    with pytest.raises(ValueError):
        run.add_measurements(measurement)

def test_zero_measurement_id_is_rejected():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=0,
        borehole_id="BH1",
        depth=3000,
        temperature=100,
        measurement_time=None,
        time_since_circulation=2
    )

    with pytest.raises(ValueError):
        run.add_measurements(measurement)

def test_negative_measurement_id_is_rejected():
    run = AnalysisRun("RUN1", "BH1", 3000, 3)

    measurement = TemperatureMeasurement(
        measurement_id=-1,
        borehole_id="BH1",
        depth=3000,
        temperature=100,
        measurement_time=None,
        time_since_circulation=2
    )

    with pytest.raises(ValueError):
        run.add_measurements(measurement)

@pytest.mark.parametrize("temperature", [
    float("nan"),
    float("inf"),
    float("-inf")
])
def test_regression_rejects_non_finite_temperatures(temperature):
    run = create_test_run()

    run.measurements[0].temperature = temperature

    correction = HornerCorrection(run)

    with pytest.raises(ValueError):
        correction.perform_regression()

def test_regression_returns_finite_coefficients():
    run = create_test_run()
    correction = HornerCorrection(run)

    slope, intercept = correction.perform_regression()

    assert np.isfinite(slope)
    assert np.isfinite(intercept)