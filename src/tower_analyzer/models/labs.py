"""Labs model - research lab upgrades."""

from __future__ import annotations

from pydantic import BaseModel, Field


class LabUpgrade(BaseModel):
    """A single lab research entry."""

    name: str = Field(description="Lab upgrade name")
    level: int = Field(default=0, ge=0, description="Current research level")
    max_level: int = Field(default=0, ge=0, description="Maximum level (0 = unknown)")
    raw_value: float = Field(default=0.0, description="Raw numeric value from save")


class Labs(BaseModel):
    """Labs section - long-term research upgrades.

    TODO: map individual lab keys once BinaryFormatter keys are decoded.
    """

    upgrades: list[LabUpgrade] = Field(
        default_factory=list,
        description="List of all lab research upgrades",
    )
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
