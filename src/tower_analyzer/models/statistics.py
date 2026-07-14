"""Statistics model - lifetime gameplay statistics."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Statistics(BaseModel):
    """Lifetime player statistics extracted from the save.

    TODO: complete field mapping once BinaryFormatter decode is finished.
    """

    total_games_played: int = Field(default=0, ge=0, description="Total number of runs played")
    total_kills: int = Field(default=0, ge=0, description="Lifetime enemy kills")
    total_waves_reached: int = Field(
        default=0, ge=0, description="Total waves reached across all runs"
    )
    highest_wave_ever: int = Field(default=0, ge=0, description="All-time highest wave")
    total_coins_earned: float = Field(default=0.0, ge=0.0, description="Lifetime coins earned")
    total_playtime_seconds: float = Field(
        default=0.0, ge=0.0, description="Total playtime in seconds"
    )
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
