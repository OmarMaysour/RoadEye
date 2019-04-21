class AccelerometerDTO:
    def __init__(self, _id, accelerometer_read_x,accelerometer_read_y, accelerometer_read_z, lat, lng, created_at):
        self.id = _id
        self.accelerometer_read_x = accelerometer_read_x
        self.accelerometer_read_y = accelerometer_read_y
        self.accelerometer_read_z = accelerometer_read_z
        self.lat = lat
        self.lng = lng
        self.created_at = created_at

    def get_values_in_dictionary(self):
        return {
            'accelerometerReadX': self.accelerometer_read_x,
            'accelerometerReadY': self.accelerometer_read_y,
            'accelerometerReadZ': self.accelerometer_read_z,
            'lat': self.lat,
            'lng': self.lng,
            'createdAt': self.created_at
        }
