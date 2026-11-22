from models.borehole import Borehole


class BoreholeController:

    def __init__(self):
        self.boreholes = {}

    def create_borehole(self, borehole_id, location, total_depth):

        if borehole_id in self.boreholes:
            raise ValueError("Borehole already exists")

        borehole = Borehole(
            borehole_id=borehole_id,
            location=location,
            total_depth=total_depth
        )

        self.boreholes[borehole_id] = borehole

        return borehole

    def get_borehole(self, borehole_id):

        if borehole_id not in self.boreholes:
            raise ValueError("Borehole not found")

        return self.boreholes[borehole_id]