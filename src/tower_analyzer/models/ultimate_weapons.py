"""UltimateWeapons model - end-game ultimate weapon data."""

from __future__ import annotations

from pydantic import BaseModel, Field


class UltimateWeapon(BaseModel):
    """A single ultimate weapon."""

    weapon_id: str = Field(description="Unique weapon identifier")
    name: str = Field(default="", description="Display name")
    level: int = Field(default=0, ge=0, description="Upgrade level")
    unlocked: bool = Field(default=False, description="Whether the weapon has been unlocked")
    raw_value: float = Field(default=0.0, description="Raw numeric value from save")


class UltimateWeapons(BaseModel):
    """UltimateWeapons section - end-game powerful weapons.

    TODO: map weapon IDs once BinaryFormatter object graph is decoded.
    """

    weapons: list[UltimateWeapon] = Field(
        default_factory=list,
        description="All ultimate weapons",
    )
    raw_fields: dict[str, object] = Field(
        default_factory=dict,
        description="Unparsed fields for forward compatibility",
    )
