from pydantic import BaseModel, Field, model_validator, ValidationError
import datetime
from enum import Enum
from typing import Optional


class Contacts(Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime.datetime
    location: str = Field(min_length=3, max_length=100)
    contact_type: Contacts
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=100)
    witness_count: int = Field(ge=1, le=100)
    message_received: Optional[str]
    is_verified: bool = Field(default=False)

    @model_validator(mode='after')
    def val_fields(self):
        if self.contact_id[0:2] != "AC":
            raise ValueError("Contact ID must start with AC \
(Alien Contact)")
        if self.contact_type == Contacts.PHYSICAL:
            if not self.is_verified:
                raise ValueError("Physical contact reports must be \
verified")
        if self.witness_count < 3:
            raise ValueError("Telepathic contact requires at least 3 \
witnesses")
        if self.signal_strength > 7:
            if not self.message_received:
                raise ValueError("Strong signals (>7.0) should include \
received messages")
        return self


if __name__ == "__main__":
    print("Alien Contact Log Validation")
    print("======================================")

    ac = AlienContact(
        contact_id="AC_2024_001",
        timestamp=datetime.datetime.now(),
        location="Area 51, Nevada",
        contact_type=Contacts.RADIO,
        signal_strength=8.5,
        duration_minutes=45,
        witness_count=5,
        message_received="Greetings from Zeta Reticuli"
    )

    print("Valid contact report:")
    print(f"ID: {ac.contact_id}")
    print(f"Type: {ac.contact_type.value}")
    print(f"Location {ac.location}")
    print(f"Signal: {ac.signal_strength}/10")
    print(f"Duration: {ac.duration_minutes} minutes")
    print(f"Witnesses: {ac.witness_count}")
    print(f"Message: {ac.message_received}")

    print("\n======================================")
    print("Expected validation error:")

    try:
        ac_error = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.datetime.now(),
            location="Area 51, Nevada",
            contact_type=Contacts.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli"
        )
        print("Valid contact report:")
        print(f"ID: {ac.contact_id}")
        print(f"Type: {ac.contact_type.value}")
        print(f"Location {ac.location}")
        print(f"Signal: {ac.signal_strength}/10")
        print(f"Duration: {ac.duration_minutes} minutes")
        print(f"Witnesses: {ac.witness_count}")
        print(f"Message: {ac.message_received}")
    except ValidationError as error:
        print(error.errors()[0]["ctx"]["error"])
