
class Borehole:
    def __init__(self, borehole_id, location, total_depth):
        self.borehole_id = borehole_id
        self.location = location
        self.total_depth = total_depth
        self.measurements = []

    def add_measurement(self, measurement):
        measurement.validate()

        if measurement.borehole_id != self.borehole_id:
            raise ValueError("Measurement belongs to another borehole")

        if measurement.depth > self.total_depth:
            raise ValueError("Measurement exceeds borehole depth")

        self.measurements.append(measurement)

    def get_measurements_at_depth(self, depth):
        return [measurement for measurement in self.measurements if measurement.depth == depth]

    def get_all_measurements(self):
        return self.measurements

    def remove_measurement(self, measurement_id):
        for measurement in self.measurements:
            if measurement.measurement_id == measurement_id:
                self.measurements.remove(measurement)
                return True
        return False
    
    def get_average_temperature_depth(self, depth):
        measurements = self.get_measurements_at_depth(depth)

        if len(measurements) == 0:
            return None

        total_temperature = sum(m.temperature for m in measurements)
        return total_temperature / len(measurements)
    
    def get_measurement_count(self):
        return len(self.measurements)

    def __str__(self):
        return (
            f"Borehole {self.borehole_id} | "
            f"Location: {self.location} | "
            f"Depth: {self.total_depth}m | "
            f"Measurements: {len(self.measurements)}"
        )
