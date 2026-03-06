from enum import Enum
from pydantic import BaseModel, Field, model_validator, ValidationError
import datetime


class Rank(Enum):
    COMMANDER = "commander"
    CAPTAIN = "captain"
    LIEUTENANT = "lieutenant"
    OFFICER = "officer"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    years_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime.datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validator(self):
        if self.mission_id[0] != 'M':
            raise ValueError("Mission ID must start with 'M'")
        commander_captain = False
        experience = 0
        for member in self.crew:
            if member.rank == Rank.COMMANDER or member.rank == Rank.CAPTAIN:
                commander_captain = True
            if not member.is_active:
                raise ValueError("All crew members must be active")
            if member.years_experience >= 5:
                experience += 1
        if not commander_captain:
            raise ValueError("Must have at least one Commander or Captain")
        if len(self.crew) / 2 > experience:
            raise ValueError("Long missions (> 365 days) need 50% experienced \
crew (+5 years)")
        return self


if __name__ == "__main__":
    print("Space Mission Crew Validation")
    print("=========================================")

    crew = [
        CrewMember(
            member_id="M_001",
            name="Sarah Connor",
            rank=Rank.COMMANDER,
            age=45,
            specialization="Mission Command",
            years_experience=20,
            is_active=True
        ),
        CrewMember(
            member_id="M_002",
            name="John Smith",
            rank=Rank.LIEUTENANT,
            age=35,
            specialization="Navigation",
            years_experience=10,
            is_active=True
        ),
        CrewMember(
            member_id="M_003",
            name="Alice Johnson",
            rank=Rank.OFFICER,
            age=55,
            specialization="Engineering",
            years_experience=30,
            is_active=True
        )
    ]
    space_mission = SpaceMission(
        mission_id="M20204_MARS",
        mission_name="Mars Colony Establishment",
        destination="Mars",
        launch_date=datetime.datetime.now(),
        duration_days=900,
        crew=crew,
        mission_status="planned",
        budget_millions=2500.0
    )

    print("Valid mission created:")
    print(f"Mission: {space_mission.mission_name}")
    print(f"ID: {space_mission.mission_id}")
    print(f"Destination: {space_mission.destination}")
    print(f"Duration: {space_mission.duration_days} days")
    print(f"Budget: ${space_mission.budget_millions}M")
    print(f"Crew size: {len(crew)}")
    print("Crew members:")
    for member in crew:
        print(f"- {member.name} ({member.rank.value}) - \
{member.specialization}")

    print("\n=========================================")
    print("Expected validation error:")
    try:
        crew = [
            CrewMember(
                member_id="M_001",
                name="Sarah Connor",
                rank=Rank.OFFICER,
                age=45,
                specialization="Mission Command",
                years_experience=20,
                is_active=True
            ),
            CrewMember(
                member_id="M_002",
                name="John Smith",
                rank=Rank.OFFICER,
                age=35,
                specialization="Navigation",
                years_experience=10,
                is_active=True
            ),
            CrewMember(
                member_id="M_003",
                name="Alice Johnson",
                rank=Rank.OFFICER,
                age=55,
                specialization="Engineering",
                years_experience=30,
                is_active=True
            )
        ]
        space_mission2 = SpaceMission(
            mission_id="M20204_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime.datetime.now(),
            duration_days=900,
            crew=crew,
            mission_status="planned",
            budget_millions=2500.0
        )
        print("Valid mission created:")
        print(f"Mission: {space_mission2.mission_name}")
        print(f"ID: {space_mission2.mission_id}")
        print(f"Destination: {space_mission2.destination}")
        print(f"Duration: {space_mission2.duration_days} days")
        print(f"Budget: ${space_mission2.budget_millions}M")
        print(f"Crew size: {len(crew)}")
        print("Crew members:")
        for member in crew:
            print(f"- {member.name} ({member.rank.value}) - \
{member.specialization}")
    except ValidationError as error:
        print(error.errors()[0]["ctx"]["error"])
