class AnomalyDTO:
    def __init__(self, frame, confidence, lat, lng, created_at):
        self.frame = frame
        self.confidence = confidence
        self.lat = lat
        self.lng = lng
        self.created_at = created_at
