"""TierProgress model - tower tier / prestige ladder progress."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TierEntry(BaseModel):
    """Progress record for a single tier."""

    tier_number: int = Field(ge=0, description="Tier number (0-indexed)")
    completed: bool = Field(default=False, description="Whether this tier has been completed")
    best_wave: int = Field(default=0, ge=0, description="Best wave reached in this tier")
    stars_earned: int = Field(default=0, ge=0, le=3, description="Stars earned (0-3)")


class TierProgress(BaseModel):
    """TierProgress section - tier-by-tier ladder completion status.

    TODO: complete mapping once BinaryFormatter decode is finished.
    """

    tiers: list[TierEntry] = Field(
        default_factory=list,
        description="Per-tier progress entries",
    )
    current_tier: int = Field(default=0, ge=0, description="The tier the player is currently on")
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
