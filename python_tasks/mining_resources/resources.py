class Resource:
    def __init__(self, name: str, manufacturer: str, total: int, allocated: int):
        self._name = name
        self._manufacturer = manufacturer
        self._total = total
        self._allocated = allocated

    @property
    def name(self) -> str:
        return self._name

    @property
    def manufacturer(self) -> str:
        return self._manufacturer

    @property
    def total(self) -> int:
        return self._total

    @property
    def allocated(self) -> int:
        return self._allocated

    def __str__(self) -> str:
        return self._name

    def __repr__(self) -> str:
        return f"{self._name}, {self._manufacturer}, {self._total}, {self._allocated}"

    def claim(self, n: int) -> None:
        if self._total - self._allocated >= n:
            self._allocated += n
        else:
            raise ValueError(
                f"Not enough '{self._name}' available to claim {n}.")

    def freeup(self, n) -> None:
        if self._allocated >= n:
            self._allocated -= n
        else:
            raise ValueError(
                f"Not enough '{self._name}' allocated to free up {n}.")

    def died(self, n) -> None:
        if self._total - self._allocated >= n:
            self._total -= n
        else:
            raise ValueError(
                f"Not enough '{self._name}' available to die {n}.")

    def purchased(self, n) -> None:
        self._total += n

    def category(self) -> str:
        return self.__class__.__name__.lower()