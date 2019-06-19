class AnomalyDTO:
    def __init__(self, _id, pothole_confidence, bump_confidence, manhole_confidence, rumble_strip_confidence
                 , lat, lng, image_uri, created_at):
        self.id = _id
        self.pothole_confidence = pothole_confidence
        self.bump_confidence = bump_confidence
        self.manhole_confidence = manhole_confidence
        self.rumbleStrip_confidence = rumble_strip_confidence
        self.lat = lat
        self.lng = lng
        self.image_uri = image_uri
        self.created_at = created_at

    def get_values_to_payload(self):
        return {
            "PotholeConfidence": self.pothole_confidence,
            "BumpConfidence": self.bump_confidence,
            "ManholeConfidence": self.manhole_confidence,
            "RumbleStripConfidence": self.rumbleStrip_confidence,
            "Type": self.get_type(),
            "Lat": self.lat,
            "Lng": self.lng,
            "CreatedAt": self.created_at
        }

    def get_type(self):
        max_confidence = max(self.pothole_confidence, self.bump_confidence, self.manhole_confidence, self.rumbleStrip_confidence)
        if max_confidence == self.pothole_confidence:
            return "Pothole"
        elif max_confidence == self.bump_confidence:
            return "Bump"
        elif max_confidence == self.manhole_confidence:
            return "Manhole"
        else:
            return "RumbleStrip"
