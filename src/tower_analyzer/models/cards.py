"""Cards model - collectible card inventory."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Card(BaseModel):
    """A single collectible card."""

    card_id: str = Field(description="Unique card identifier")
    name: str = Field(default="", description="Display name")
    level: int = Field(default=0, ge=0, description="Current card level")
    copies: int = Field(default=0, ge=0, description="Number of copies owned")
    raw_value: float = Field(default=0.0, description="Raw numeric bonus value from save")


class Cards(BaseModel):
    """Cards section - collectible cards and their levels.

    TODO: map card IDs to human-readable names once decode is complete.
    """

    cards: list[Card] = Field(default_factory=list, description="All cards in inventory")
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
