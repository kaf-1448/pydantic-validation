from pydantic import BaseModel, Field, ValidationError
from pydantic import model_validator
from typing import Optional
from datetime import datetime
from enum import Enum


class ContactType(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PYHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100)

    contact_type: ContactType

    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1400)
    witness_count: int = Field(ge=1, le=100)

    message_received: Optional[str] = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def check_contact_id(self):

        if not self.contact_id.startswith("AC"):
            raise ValueError("contact_id must be start by AC")

        return self

    @model_validator(mode="after")
    def check_contact_type(self):

        if self.contact_type == ContactType.PYHYSICAL and not (
                self.is_verified):
            raise ValueError("Physical contact reports must be verified")

        return self

    @model_validator(mode="after")
    def check_witness_count(self):

        if self.contact_type == ContactType.TELEPATHIC and (
                self.witness_count < 3):

            raise ValueError(
                "Telepathic contact requires at least 3 witnesses")

        return self

    @model_validator(mode="after")
    def check_signal_strength(self):

        if self.signal_strength > 7 and not (
                self.message_received):

            raise ValueError(
                "should include received messages")

        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("========================================")
    print("Valid contact report:")

    report = AlienContact(
        contact_id="AC_2024_001",
        contact_type="radio",
        timestamp=datetime.now(),
        location="rea 51, Nevada",
        signal_strength="8.5",
        duration_minutes=45,
        witness_count="5",
        message_received="Greetings from Zeta Reticuli"
    )

    print(f"ID: {report.contact_id}")
    print(f"Type: {report.contact_type.value}")
    print(f"Location: {report.location}")
    print(f"Signal: {report.signal_strength}/10")
    print(f"Duration: {report.duration_minutes} minutes")
    print(f"Witnesses: {report.witness_count}")
    print(f"Message: '{report.message_received}'")

    try:
        print("\n========================================")
        print("Expected validation error:")

        report = AlienContact(
            contact_id="AC_2024_001",
            contact_type="telepathic",
            timestamp=datetime.now(),
            location="rea 51, Nevada",
            signal_strength="8.5",
            duration_minutes=45,
            witness_count="2",
            message_received="Greetings from Zeta Reticuli"
        )
        print(f"witness: {report.witness_count}")

    except ValidationError as e:
        for error in e.errors():
            print(error['ctx']['error'])


if __name__ == "__main__":
    main()
