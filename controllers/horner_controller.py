from models.analysis_run import AnalysisRun
from models.temperature_measurement import TemperatureMeasurement
from models.horner_correction import HornerCorrection


class HornerController:

    def __init__(self):
        self.analysis_run = None
        self.horner_engine = None

    def create_analysis_run(self, run_id, borehole_id, depth, circulation_time):
        self.analysis_run = AnalysisRun(
            run_id,
            borehole_id,
            depth,
            circulation_time
        )

        self.horner_engine = HornerCorrection(self.analysis_run)

        return self.analysis_run

    def add_measurements(self, measurements):
        for measurement in measurements:
            new_measurement = TemperatureMeasurement(
                measurement_id=measurement["measurement_id"],
                borehole_id=self.analysis_run.borehole_id,
                depth=measurement["depth"],
                temperature=measurement["temperature"],
                measurement_time=measurement.get("measurement_time"),
                time_since_circulation=measurement["time_since_circulation"]
        )
            self.analysis_run.add_measurements(new_measurement)

    def perform_analysis(self):
        if self.horner_engine is None:
            raise ValueError("No analysis run has been created")

        slope, intercept = self.horner_engine.perform_regression()

        static_temperature = self.horner_engine.calculate_static_formation_temperature()

        return {
            "slope": slope,
            "intercept": intercept,
            "static_formation_temperature": static_temperature
        }

    