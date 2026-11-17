from datetime import datetime

class TemperatureMeasurement:
    def __init__(self,
        measurement_id: str,
        borehole_id: str,
        depth: int,
        temperature: float,
        measurement_time: datetime,
        time_since_circulation: float,
        measurement_uncertainty=None,
        instrument_id=None):

        self.measurement_id = measurement_id
        self.borehole_id = borehole_id
        self.depth = depth
        self.temperature = temperature
        self.measurement_time = measurement_time
        self.time_since_circulation = time_since_circulation
        self.measurement_uncertainty = measurement_uncertainty
        self.instrument_id = instrument_id

    def validate(self):

        if self.depth <= 0:
            raise ValueError("Depth must be positive")

        if self.temperature < -273.15:
            raise ValueError("Temperature below absolute zero")

        if self.time_since_circulation <= 0:
            raise ValueError("Elapsed time must be positive")

        if self.measurement_uncertainty is not None:
            if self.measurement_uncertainty < 0:
                raise ValueError("Uncertainty cannot be negative")

    def __str__(self):
        return (
            f"Measurement {self.measurement_id}: "
            f"{self.temperature}°C at "
            f"{self.depth}m"
        )


measurements1 = TemperatureMeasurement("MH001", "BH001", 1500, 45.2, datetime.now(), 13)
measurements2 = TemperatureMeasurement("MH002", "BH001", 1500, 46.1, datetime.now(), 14)

measurements = [measurements1, measurements2]

for measurement in measurements:
    print(measurement)
