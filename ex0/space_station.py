from pydantic import BaseModel, Field, ValidationError
import datetime
from typing import Optional


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime.datetime
    is_operational: bool = Field(default=True)
    notes: Optional[str] = Field(default=None, max_length=200)


if __name__ == "__main__":
    print("Space Station Data Validation")
    print("========================================")

    space_stat = SpaceStation(station_id="ISS001", name="International Space"
                              " Station", crew_size=6, power_level=85.5,
                              oxygen_level=92.3,
                              last_maintenance='2032-04-23T10:20:30.400+02:30',
                              is_operational=True)
    print("Valid station created:")
    print(f"ID: {space_stat.station_id}")
    print(f"Name: {space_stat.name}")
    print(f"Crew: {space_stat.crew_size} people")
    print(f"Power: {space_stat.power_level}%")
    print(f"Oxygen: {space_stat.oxygen_level}%")
    if space_stat.is_operational:
        print("Status: Operational")
    else:
        print("Status: Non-Operational")

    print("\n========================================")
    print("Expected validation error:")
    try:
        SpaceStation(
            station_id="A",
            name="Test",
            crew_size=21,
            power_level=-1,
            oxygen_level=1000,
            last_maintenance='2032-04-23T10:20:30.400+02:30',
            is_operational=True
        )
    except ValidationError as error:
        print(error.errors()[0]["msg"])
