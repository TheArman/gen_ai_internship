from storage import Storage


class HDD(Storage):
    def __init__(self, name: str, manufacturer: str, total: int,
                 allocated: int, capacity_GB: int, size: int, rpm: int) -> None:
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self._size = size
        self._rpm = rpm

    @property
    def size(self) -> int:
        return self._size

    @property
    def rpm(self) -> int:
        return self._rpm