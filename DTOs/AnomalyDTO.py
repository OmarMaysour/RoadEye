class AnomalyDTO:
    def __init__(self, _id, pothole_confidence, bump_confidence, manhole_confidence, road_crack_confidence
                 , lat, lng, image_uri, created_at):
        self.id = _id
        self.pothole_confidence = pothole_confidence
        self.bump_confidence = bump_confidence
        self.manhole_confidence = manhole_confidence
        self.roadCrack_confidence = road_crack_confidence
        self.lat = lat
        self.lng = lng
        self.image_uri = image_uri
        self.created_at = created_at

    def get_values_in_dictionary(self):
        return {
            'potholeConfidence': self.pothole_confidence,
            'bumpConfidence': self.bump_confidence,
            'manholeConfidence': self.manhole_confidence,
            'roadCrackConfidence': self.roadCrack_confidence,
            'lat': self.lat,
            'lng': self.lng,
            'image_id': self.image_uri,
            'createdAt': self.created_at
        }