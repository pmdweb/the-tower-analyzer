"""Economy model - currency balances and income tracking."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Economy(BaseModel):
    """Economy section - currency and resource balances.

    TODO: complete field mapping once BinaryFormatter decode is finished.
    """

    coins: float = Field(default=0.0, ge=0.0, description="Current coin balance")
    gems: int = Field(default=0, ge=0, description="Current gem balance")
    free_gems_earned: int = Field(default=0, ge=0, description="Total free gems ever earned")
    keys: int = Field(default=0, ge=0, description="Current key count")
    dust: int = Field(default=0, ge=0, description="Current dust (card upgrade material)")
    orbs: int = Field(default=0, ge=0, description="Current orb count")
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
