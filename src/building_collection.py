class BuildingCollection:
    def __init__(self, council_bbox, pages):
        self.pages = pages
    def produce_list(self):
        if self.pages != 0:
            return [None] * (self.pages * 100)
        return []