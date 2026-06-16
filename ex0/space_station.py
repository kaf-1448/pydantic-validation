from pydantic import BaseModel, Field, ValidationError
from datetime import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


def main() -> None:
    try:
        print("Space Station Data Validation")
        print("========================================")
        print("Valid station created:")

        space_station = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size="6",
            power_level="85.5",
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            notes=None
        )

        print(f"ID: {space_station.station_id}")
        print(f"Name: {space_station.name}")
        print(f"Crew: {space_station.crew_size}")
        print(f"Power: {space_station.power_level}%")
        print(f"Oxygen: {space_station.oxygen_level}%")
        status: str = 'Operational' if space_station.is_operational else "Offline"
        print(f"Status:{status}")

        print("\n========================================")
        print("Expected validation error:")
        e_space_s = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size="21",
            power_level="85.5",
            oxygen_level=92.3,
            last_maintenance=datetime.now(),
            notes="Operational"
        )

        print(f"crew_size{e_space_s.crew_size}")

    except ValidationError as e:
        print(e)


if __name__ == "__main__":
    main()
