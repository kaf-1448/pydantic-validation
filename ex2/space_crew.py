from pydantic import BaseModel, Field, ValidationError
from pydantic import model_validator
from datetime import datetime
from enum import Enum


class Rank(Enum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


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

    launch_date: datetime

    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)

    mission_status: str = Field(default="planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_mission_id(self):

        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with \"M\"")

        return self

    @model_validator(mode="after")
    def check_members(self):

        is_there = False

        for mem in self.crew:
            if mem.rank == Rank.COMMANDER or mem.rank == Rank.CAPTAIN:
                is_there = True

        if not is_there:
            raise ValueError("Must have at least one Commander or Captain")

        return self

    @model_validator(mode="after")
    def check_duration(self):
        mumber = 0

        for crew in self.crew:
            if crew.years_experience >= 5:
                mumber += 1

        if (self.duration_days > 365
                and len(self.crew) / 2 > mumber):

            raise ValueError(
                "Long missions (> 365 days) need 50% "
                "experienced crew (5+ years)")

        return self

    @model_validator(mode="after")
    def check_is_active(self):

        active = True

        for crew in self.crew:
            if not crew.is_active:
                active = False

        if not active:
            raise ValueError(
                "All crew members must be active")

        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================")
    print("Valid mission created:")

    mission = SpaceMission(
        mission_name="Mars Colony Establishment",
        mission_id="M2024_MARS",
        destination="Mars",
        launch_date=datetime.now(),
        duration_days=900,
        crew=[
            CrewMember(
                member_id="M00",
                name="Sarah Connor",
                rank=Rank.COMMANDER,
                age=19,
                specialization="Mission Command",
                years_experience=15,
                is_active=True,
            ),
            CrewMember(
                member_id="M02",
                name="john Smit",
                rank=Rank.LIEUTENANT,
                age=57,
                specialization="Navigation",
                years_experience=25,
                is_active=True,
            ),
            CrewMember(
                member_id="M03",
                name="Alice Johnso",
                rank=Rank.OFFICER,
                age=57,
                specialization="Engineering",
                years_experience=35,
                is_active=True,
            ),
        ],
        mission_status="planned",
        budget_millions=2500,
    )

    print(f"Mission: {mission.mission_id}")
    print(f"ID: {mission.mission_name}")
    print(f"Destination: {mission.destination}")
    print(f"Duration: {mission.duration_days}days")
    print(f"Budget: {mission.budget_millions}M")
    print(f"crew size: {len(mission.crew)}")
    print("Crew members:")
    for ind in mission.crew:
        print(f"- {ind.name} ({ind.rank.value}) - {ind.specialization}")

    try:
        print("\n========================================")
        print("Expected validation error:")

        mission = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime.now(),
            duration_days=900,
            crew=[
                CrewMember(
                    member_id="M00",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=19,
                    specialization="Mission Command",
                    years_experience=15,
                    is_active=True,
                ),
                CrewMember(
                    member_id="M02",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=57,
                    specialization="Navigation",
                    years_experience=25,
                    is_active=True,
                ),
            ],
            mission_status="planned",
            budget_millions=2500,
        )

    except ValidationError as e:
        for error in e.errors():
            print(error['ctx']['error'])


if __name__ == "__main__":
    main()
