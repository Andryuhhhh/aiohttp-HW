from pydantic import BaseModel, Field, field_validator


class AdvertBase(BaseModel):
    title: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=255)

    @field_validator("title", "description", mode="before")
    @classmethod
    def validate_not_empty(cls, value: object) -> str:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Field is required and cannot be empty")
        return value.strip()


class AdvertCreate(AdvertBase):
    owner: str


class AdvertUpdate(AdvertBase):
    owner: str | None = None
