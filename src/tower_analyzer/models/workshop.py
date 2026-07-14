"""Workshop model - tower upgrade levels and their costs."""

from __future__ import annotations

from pydantic import BaseModel, Field


class WorkshopUpgrade(BaseModel):
    """A single workshop upgrade entry."""

    name: str = Field(description="Upgrade name")
    level: int = Field(default=0, ge=0, description="Current upgrade level")
    max_level: int = Field(default=0, ge=0, description="Maximum upgrade level (0 = unknown)")
    raw_value: float = Field(default=0.0, description="Raw numeric value from save")


class Workshop(BaseModel):
    """Workshop section - tower permanent upgrades.

    TODO: map individual upgrade keys once BinaryFormatter keys are decoded.
    """

    upgrades: list[WorkshopUpgrade] = Field(
        default_factory=list,
        description="List of all workshop upgrades",
    )
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
