
from models.borehole import Borehole
from models.temperature_measurement import TemperatureMeasurement
from datetime import datetime

# Create a borehole
borehole = Borehole(
    borehole_id="BH001",
    location="London",
    total_depth=1500
)

# Create measurements
m1 = TemperatureMeasurement(
    "M001", "BH001", 500, 45.2,
    datetime.now(), 2.0
)

m2 = TemperatureMeasurement(
    "M002", "BH001", 500, 46.1,
    datetime.now(), 4.0
)

m3 = TemperatureMeasurement(
    "M003", "BH001", 1000, 65.4,
    datetime.now(), 2.0
)

# Add measurements to borehole
borehole.add_measurement(m1)
borehole.add_measurement(m2)
borehole.add_measurement(m3)

# Retrieve measurements at 500m
results = borehole.get_measurements_at_depth(500)

print(borehole)

for measurement in results:
    print(measurement)
