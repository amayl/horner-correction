from controllers.horner_controller import HornerController
from controllers.borehole_controller import BoreholeController

import math
import pytest

def test_create_analysis_run():
    controller = HornerController()

    run = controller.create_analysis_run(
        run_id="RUN1",
        borehole_id="BH1",
        depth=3000,
        circulation_time=3
    )

    assert run.run_id == "RUN1"
    assert run.borehole_id == "BH1"
    assert run.depth == 3000
    assert run.circulation_time == 3

    assert controller.analysis_run is run
    assert controller.horner_engine is not None

def test_add_measurements():
    controller = HornerController()

    controller.create_analysis_run(
        "RUN1", "BH1", 3000, 3
    )

    measurements = [
        {
            "measurement_id": 1,
            "depth": 3000,
            "temperature": 90.0,
            "measurement_time": None,
            "time_since_circulation": 1
        },
        {
            "measurement_id": 2,
            "depth": 3000,
            "temperature": 92.0,
            "measurement_time": None,
            "time_since_circulation": 2
        },
        {
            "measurement_id": 3,
            "depth": 3000,
            "temperature": 94.0,
            "measurement_time": None,
            "time_since_circulation": 3
        }
    ]

    controller.add_measurements(measurements)

    assert len(controller.analysis_run.measurements) == 3

    assert controller.analysis_run.measurements[0].temperature == 90.0
    assert controller.analysis_run.measurements[1].temperature == 92.0
    assert controller.analysis_run.measurements[2].temperature == 94.0

def test_perform_analysis():
    controller = HornerController()

    controller.create_analysis_run(
        "RUN1", "BH1", 3000, 3
    )

    measurements = []

    for i, shut_in_time in enumerate([1, 2, 3, 4, 5], start=1):
        temperature = 100 - 10 * math.log(
            (3 + shut_in_time) / shut_in_time
        )

        measurements.append({
            "measurement_id": i,
            "depth": 3000,
            "temperature": temperature,
            "measurement_time": None,
            "time_since_circulation": shut_in_time
        })

    controller.add_measurements(measurements)

    results = controller.perform_analysis()

    assert results["slope"] == pytest.approx(-10)
    assert results["intercept"] == pytest.approx(100)
    assert results["static_formation_temperature"] == pytest.approx(100)

def test_create_borehole():

    controller = BoreholeController()

    borehole = controller.create_borehole(
        "BH001",
        "Southall",
        3000
    )

    assert borehole.borehole_id == "BH001"
    assert borehole.location == "Southall"
    assert borehole.total_depth == 3000

    assert "BH001" in controller.boreholes
    assert controller.boreholes["BH001"] is borehole

def test_duplicate_borehole_id():

    controller = BoreholeController()

    controller.create_borehole(
        "BH001",
        "Southall",
        3000
    )

    with pytest.raises(ValueError, match="Borehole already exists"):
        controller.create_borehole(
            "BH001",
            "London",
            2500
        )

def test_get_borehole():

    controller = BoreholeController()

    created_borehole = controller.create_borehole(
        "BH001",
        "Southall",
        3000
    )

    retrieved_borehole = controller.get_borehole("BH001")

    assert retrieved_borehole is created_borehole

def test_get_nonexistent_borehole():

    controller = BoreholeController()

    with pytest.raises(ValueError, match="Borehole not found"):
        controller.get_borehole("BH999")