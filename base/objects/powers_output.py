from dataclasses import asdict, dataclass


@dataclass
class PowerPropertyDisplay:
    title: str
    description: str
    debug: str | None = None


@dataclass
class PowerDisplay:
    name: str
    keywords: str
    category: str
    description: str
    frequency_order: int
    frequency: str
    properties: list[PowerPropertyDisplay]

    def asdict(self) -> dict:
        return asdict(self)
