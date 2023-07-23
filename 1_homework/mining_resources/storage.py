from resources import Resource


class Storage(Resource):
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int, capacity_GB: int) -> None:
        super().__init__(name, manufacturer, total, allocated)
        self._capacity_GB = capacity_GB

    @property
    def capacity_GB(self) -> int:
        return self._capacity_GB