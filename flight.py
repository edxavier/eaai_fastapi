from dataclasses import dataclass



@dataclass
class Flight:
    logo: str
    flight: str
    origin: str
    time: str
    status: str
    gate: str
