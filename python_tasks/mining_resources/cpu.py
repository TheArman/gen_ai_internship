from resources import Resource


class CPU(Resource):
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int,
                 core: int, interface: str, socket: str, power_watts: int) -> None:
        super().__init__(name, manufacturer, total, allocated)
        self._core = core
        self._socket = socket
        self._interface = interface
        self._power_watts = power_watts

    @property
    def core(self) -> int:
        return self._core

    @property
    def socket(self) -> str:
        return self._socket

    @property
    def interface(self) -> str:
        return self._interface

    @property
    def power_watts(self) -> int:
        return self._power_watts