"""Modules model - equippable tower modules."""

from __future__ import annotations

from pydantic import BaseModel, Field


class Module(BaseModel):
    """A single equippable module."""

    module_id: str = Field(description="Unique module identifier")
    name: str = Field(default="", description="Display name")
    tier: int = Field(default=0, ge=0, description="Module tier / rarity")
    level: int = Field(default=0, ge=0, description="Upgrade level")
    equipped: bool = Field(default=False, description="Whether the module is currently equipped")
    raw_value: float = Field(default=0.0, description="Raw numeric value from save")


class Modules(BaseModel):
    """Modules section - equippable tower modules inventory.

    TODO: map module IDs once BinaryFormatter object graph is decoded.
    """

    modules: list[Module] = Field(default_factory=list, description="All modules owned")
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
