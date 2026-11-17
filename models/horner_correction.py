import numpy as np

class HornerCorrection:
    def __init__(self, analysis_run):
        self.analysis_run = analysis_run

    def calculate_horner_ratio(self, shut_in_time):
        if shut_in_time <= 0:
                    raise ValueError("Shut-in time must be greater than 0")
        if self.analysis_run.circulation_time <= 0:
            raise ValueError("Circulation time must be greater than 0")
        return (self.analysis_run.circulation_time + shut_in_time) / shut_in_time

    def calculate_log_horner_ratio(self, shut_in_time):
        if shut_in_time <= 0:
            raise ValueError("Shut-in time must be greater than 0")
        return np.log(self.calculate_horner_ratio(shut_in_time))

    def prepare_regression_data(self):
        x_values, y_values = [], []

        for measurement in self.analysis_run.measurements:
            x_i = self.calculate_log_horner_ratio(measurement.time_since_circulation)
            x_values.append(x_i)

            temperature = measurement.temperature
            y_values.append(temperature)
        return x_values, y_values

    def perform_regression(self):
        x_values, y_values = self.prepare_regression_data()
        
        if not self.analysis_run.is_ready_for_analysis():
            raise ValueError("Insufficient values for regression")

        if len(set(x_values)) < 2:
            raise ValueError("At least two distinct Horner values are required")

        slope, intercept = np.polyfit(x_values, y_values, 1)
        return slope, intercept

    def calculate_static_formation_temperature(self):
        slope, intercept = self.perform_regression()
        return intercept
    