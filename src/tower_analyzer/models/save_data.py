"""Top-level SaveData model aggregating all parsed sections."""

from __future__ import annotations

from datetime import UTC, datetime

from pydantic import BaseModel, Field

from tower_analyzer.models.cards import Cards
from tower_analyzer.models.economy import Economy
from tower_analyzer.models.labs import Labs
from tower_analyzer.models.modules import Modules
from tower_analyzer.models.player_account import PlayerAccount
from tower_analyzer.models.statistics import Statistics
from tower_analyzer.models.tier_progress import TierProgress
from tower_analyzer.models.ultimate_weapons import UltimateWeapons
from tower_analyzer.models.workshop import Workshop


class SaveData(BaseModel):
    """Complete parsed save data.

    Aggregates all sections of a playerInfo.dat save file.
    Fields will be populated progressively as the parser is improved.
    """

    # Metadata about the parse itself, not the game data
    source_file: str = Field(default="", description="Path to the source .dat file")
    parsed_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="UTC timestamp when this file was parsed",
    )
    parse_warnings: list[str] = Field(
        default_factory=list,
        description="Non-fatal warnings encountered during parsing",
    )
    raw_bytes_size: int = Field(
        default=0,
        ge=0,
        description="Size of the original file in bytes",
    )

    # Game data sections
    account: PlayerAccount = Field(default_factory=PlayerAccount)
    workshop: Workshop = Field(default_factory=Workshop)
    labs: Labs = Field(default_factory=Labs)
    cards: Cards = Field(default_factory=Cards)
    modules: Modules = Field(default_factory=Modules)
    ultimate_weapons: UltimateWeapons = Field(default_factory=UltimateWeapons)
    statistics: Statistics = Field(default_factory=Statistics)
    economy: Economy = Field(default_factory=Economy)
    tier_progress: TierProgress = Field(default_factory=TierProgress)
