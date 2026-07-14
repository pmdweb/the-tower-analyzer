"""SaveComparator - diff two parsed SaveData snapshots.

Status: INCOMPLETE - full comparison requires complete BinaryFormatter decode.

TODO:
    1. Compare Workshop upgrade levels between old and new save.
    2. Compare Labs research levels.
    3. Compare Economy balances.
    4. Generate a structured diff for the report engine.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from tower_analyzer.models.save_data import SaveData


@dataclass
class SaveDiff:
    """Structured diff between two SaveData snapshots."""

    old_source: str
    new_source: str
    # TODO: add typed diff fields once model field mapping is complete.
    notes: list[str] = field(default_factory=list)


class SaveComparator:
    """Compare two SaveData snapshots and return a structured diff.

    Usage::

        comparator = SaveComparator()
        diff = comparator.compare(old_save, new_save)
    """

    def compare(self, old: SaveData, new: SaveData) -> SaveDiff:
        """Compare *old* and *new* save data.

        Parameters
        ----------
        old:
            Earlier save snapshot.
        new:
            Later save snapshot.

        Returns
        -------
        SaveDiff
            Structured diff.  Currently only metadata is compared; full field
            comparison is pending BinaryFormatter decode completion.
        """
        diff = SaveDiff(old_source=old.source_file, new_source=new.source_file)
        diff.notes.append(
            "Full save comparison is not yet implemented. "
            "Pending BinaryFormatter field mapping completion."
        )

        # Shallow placeholder comparisons
        if old.account.level != new.account.level:
            diff.notes.append(
                f"Level changed: {old.account.level} → {new.account.level}"
            )
        if old.account.prestige != new.account.prestige:
            diff.notes.append(
                f"Prestige changed: {old.account.prestige} → {new.account.prestige}"
            )
        if old.account.highest_wave != new.account.highest_wave:
            diff.notes.append(
                f"Highest wave changed: {old.account.highest_wave} → {new.account.highest_wave}"
            )

        return diff
