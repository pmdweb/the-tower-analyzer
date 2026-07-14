"""PlayerAccount model - basic player identity and progression."""

from __future__ import annotations

from pydantic import BaseModel, Field


class PlayerAccount(BaseModel):
    """Top-level player identity and account metadata.

    Fields are placeholders pending full BinaryFormatter decoding.
    TODO: populate from SaveLoad.PlayerData once decoder is complete.
    """

    player_name: str = Field(default="", description="In-game player name")
    player_id: str = Field(default="", description="Unique player identifier")
    level: int = Field(default=0, ge=0, description="Current player level")
    prestige: int = Field(default=0, ge=0, description="Number of prestiges completed")
    coins: float = Field(default=0.0, ge=0.0, description="Current coin balance")
    gems: int = Field(default=0, ge=0, description="Current gem balance")
    kills: int = Field(default=0, ge=0, description="Total lifetime kills")
    highest_wave: int = Field(default=0, ge=0, description="Highest wave ever reached")
    game_version: str = Field(default="", description="Game version that wrote this save")
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields from the raw save object for forward compatibility",
    )
