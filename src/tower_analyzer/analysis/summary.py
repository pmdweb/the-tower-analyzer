"""SaveSummary - produce a concise summary of a parsed SaveData."""

from __future__ import annotations

from dataclasses import dataclass

from tower_analyzer.models.save_data import SaveData


@dataclass
class SaveSummary:
    """A concise human-readable summary derived from a :class:`SaveData`.

    TODO: populate all fields once BinaryFormatter decoding is complete.
    """

    player_name: str
    level: int
    prestige: int
    highest_wave: int
    parse_warnings: list[str]

    @classmethod
    def from_save_data(cls, save: SaveData) -> SaveSummary:
        """Create a :class:`SaveSummary` from a :class:`SaveData`.

        Parameters
        ----------
        save:
            Parsed save data.

        Returns
        -------
        SaveSummary
        """
        return cls(
            player_name=save.account.player_name or "(unknown)",
            level=save.account.level,
            prestige=save.account.prestige,
            highest_wave=save.account.highest_wave,
            parse_warnings=list(save.parse_warnings),
        )
