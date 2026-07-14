"""Tests for save analysis components."""

from __future__ import annotations

from tower_analyzer.analysis.comparator import SaveComparator, SaveDiff
from tower_analyzer.analysis.summary import SaveSummary
from tower_analyzer.models.player_account import PlayerAccount
from tower_analyzer.models.save_data import SaveData


class TestSaveSummary:
    def test_from_save_data_defaults(self, empty_save_data: SaveData) -> None:
        summary = SaveSummary.from_save_data(empty_save_data)
        assert summary.player_name == "(unknown)"
        assert summary.level == 0
        assert summary.prestige == 0
        assert summary.highest_wave == 0

    def test_from_save_data_with_name(self) -> None:
        save = SaveData(source_file="t.dat")
        save.account = PlayerAccount(player_name="Dave", level=10, prestige=1, highest_wave=200)
        summary = SaveSummary.from_save_data(save)
        assert summary.player_name == "Dave"
        assert summary.level == 10
        assert summary.highest_wave == 200

    def test_warnings_propagated(self) -> None:
        save = SaveData(source_file="t.dat", parse_warnings=["warn1"])
        summary = SaveSummary.from_save_data(save)
        assert "warn1" in summary.parse_warnings


class TestSaveComparator:
    def test_compare_returns_diff(self) -> None:
        old = SaveData(source_file="old.dat")
        new = SaveData(source_file="new.dat")
        comparator = SaveComparator()
        diff = comparator.compare(old, new)
        assert isinstance(diff, SaveDiff)

    def test_compare_records_sources(self) -> None:
        old = SaveData(source_file="old.dat")
        new = SaveData(source_file="new.dat")
        comparator = SaveComparator()
        diff = comparator.compare(old, new)
        assert diff.old_source == "old.dat"
        assert diff.new_source == "new.dat"

    def test_compare_detects_level_change(self) -> None:
        old = SaveData(source_file="old.dat")
        old.account = PlayerAccount(level=5)
        new = SaveData(source_file="new.dat")
        new.account = PlayerAccount(level=10)
        comparator = SaveComparator()
        diff = comparator.compare(old, new)
        level_notes = [n for n in diff.notes if "Level" in n]
        assert len(level_notes) == 1

    def test_compare_no_change_has_incomplete_note(self) -> None:
        save = SaveData(source_file="save.dat")
        comparator = SaveComparator()
        diff = comparator.compare(save, save)
        assert any("not yet implemented" in n.lower() for n in diff.notes)
