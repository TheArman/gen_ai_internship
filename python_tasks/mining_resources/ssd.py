from storage import Storage


class SSD(Storage):
    def __init__(self, name: str, manufacturer: str, total: int,
                 allocated: int, capacity_GB: int, interface: str) -> None:
        super().__init__(name, manufacturer, total, allocated, capacity_GB)
        self._interface = interface

    @property
    def interface(self) -> str:
        return self._interface