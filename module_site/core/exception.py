class GenoTypeRangeException(Exception):
    def __init__(self, order):
        msg = "sum of each operator ratio have to be 1"
        super().__init__(msg)
