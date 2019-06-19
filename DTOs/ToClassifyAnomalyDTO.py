class ToClassifyAnomalyDTO:
    def __init__(self, _id, lat, lng, image_uri, created_at):
        self.id = _id
        self.lat = lat
        self.lng = lng
        self.image_uri = image_uri
        self.created_at = created_at
