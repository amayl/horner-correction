class AnalysisRun:
    def __init__(self, run_id, borehole_id, depth, circulation_time):
        self.run_id = run_id
        self.borehole_id = borehole_id
        self.depth = depth
        self.circulation_time = circulation_time
        self.measurements = []

        if circulation_time <= 0:
            raise ValueError("Circulation time must be greater than 0")

    def add_measurements(self, measurement):
        measurement.validate()
    
        if measurement.borehole_id != self.borehole_id:
            raise ValueError("Measurement belongs to another borehole")

        if measurement.depth != self.depth:
            raise ValueError("Measurement belongs to another depth")

        self.measurements.append(measurement)

    def get_measurements_at_depth(self):
        return self.measurements

    def is_ready_for_analysis(self):
        return len(self.measurements) >= 3