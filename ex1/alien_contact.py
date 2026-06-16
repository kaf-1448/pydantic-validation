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
    def check_contact_id(cls, model):
        if not model.contact_id.startswith("AC"):
            raise ValueError("contact_id must be start by AC")
        return model

    @model_validator(mode="after")
    def check_contact_type(cls, model):
        if model.contact_type != "physical" and not model.is_verified:
            model.is_verified = True
        return model


def main() -> None:
    print("Alien Contact Log Validation")
    print("======================================")


if __name__ == "__main__":
    main()

print(ContactType.PYHYSICAL)
