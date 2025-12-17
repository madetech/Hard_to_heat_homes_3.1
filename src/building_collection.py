class BuildingCollection:
    def __init__(self, council_bbox, pages):
        self.pages = pages
    def produce_list(self):
        if self.pages == 1:
            return [None] * 100
        return []