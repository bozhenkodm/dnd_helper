from dataclasses import dataclass


@dataclass
class PowerPropertyDisplay:
    title: str
    description: str
    debug: str


@dataclass
class PowerDisplay:
    name: str
    keywords: str
    accessory_text: str
    description: str
    frequency_order: int
    properties: list[PowerPropertyDisplay]
