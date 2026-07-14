"""Tests for Pydantic data models."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from tower_analyzer.models.cards import Card, Cards
from tower_analyzer.models.economy import Economy
from tower_analyzer.models.labs import Labs, LabUpgrade
from tower_analyzer.models.modules import Module, Modules
from tower_analyzer.models.player_account import PlayerAccount
from tower_analyzer.models.save_data import SaveData
from tower_analyzer.models.statistics import Statistics
from tower_analyzer.models.tier_progress import TierEntry, TierProgress
from tower_analyzer.models.ultimate_weapons import UltimateWeapon, UltimateWeapons
from tower_analyzer.models.workshop import Workshop, WorkshopUpgrade


class TestPlayerAccount:
    def test_defaults(self) -> None:
        account = PlayerAccount()
        assert account.level == 0
        assert account.prestige == 0
        assert account.coins == 0.0

    def test_valid_construction(self) -> None:
        account = PlayerAccount(player_name="Alice", level=42, prestige=3)
        assert account.player_name == "Alice"
        assert account.level == 42

    def test_negative_level_rejected(self) -> None:
        with pytest.raises(ValidationError):
            PlayerAccount(level=-1)


class TestWorkshop:
    def test_empty_workshop(self) -> None:
        ws = Workshop()
        assert ws.upgrades == []

    def test_with_upgrades(self) -> None:
        ws = Workshop(upgrades=[WorkshopUpgrade(name="Damage", level=10)])
        assert len(ws.upgrades) == 1
        assert ws.upgrades[0].name == "Damage"


class TestLabs:
    def test_empty_labs(self) -> None:
        labs = Labs()
        assert labs.upgrades == []

    def test_with_upgrade(self) -> None:
        labs = Labs(upgrades=[LabUpgrade(name="Lab Speed", level=5)])
        assert labs.upgrades[0].level == 5


class TestCards:
    def test_empty_cards(self) -> None:
        cards = Cards()
        assert cards.cards == []

    def test_with_card(self) -> None:
        cards = Cards(cards=[Card(card_id="c001", name="Tower Shield", level=2, copies=3)])
        assert cards.cards[0].copies == 3


class TestModules:
    def test_empty_modules(self) -> None:
        modules = Modules()
        assert modules.modules == []

    def test_with_module(self) -> None:
        mod = Module(module_id="m001", name="Attack Module", tier=2, level=5, equipped=True)
        modules = Modules(modules=[mod])
        assert modules.modules[0].equipped is True


class TestUltimateWeapons:
    def test_empty_weapons(self) -> None:
        uw = UltimateWeapons()
        assert uw.weapons == []

    def test_with_weapon(self) -> None:
        w = UltimateWeapon(weapon_id="uw001", name="Orbital Strike", unlocked=True)
        uw = UltimateWeapons(weapons=[w])
        assert uw.weapons[0].unlocked is True


class TestStatistics:
    def test_defaults(self) -> None:
        stats = Statistics()
        assert stats.total_kills == 0
        assert stats.total_playtime_seconds == 0.0

    def test_negative_kills_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Statistics(total_kills=-1)


class TestEconomy:
    def test_defaults(self) -> None:
        eco = Economy()
        assert eco.coins == 0.0
        assert eco.gems == 0

    def test_negative_coins_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Economy(coins=-100.0)


class TestTierProgress:
    def test_defaults(self) -> None:
        tp = TierProgress()
        assert tp.tiers == []
        assert tp.current_tier == 0

    def test_stars_clamped(self) -> None:
        with pytest.raises(ValidationError):
            TierEntry(tier_number=1, stars_earned=4)


class TestSaveData:
    def test_default_construction(self) -> None:
        save = SaveData(source_file="test.dat")
        assert save.source_file == "test.dat"
        assert isinstance(save.account, PlayerAccount)
        assert isinstance(save.workshop, Workshop)
        assert isinstance(save.labs, Labs)
        assert isinstance(save.cards, Cards)
        assert isinstance(save.modules, Modules)
        assert isinstance(save.ultimate_weapons, UltimateWeapons)
        assert isinstance(save.statistics, Statistics)
        assert isinstance(save.economy, Economy)
        assert isinstance(save.tier_progress, TierProgress)

    def test_json_roundtrip(self) -> None:
        """SaveData should survive a model_dump / model_validate roundtrip."""
        save = SaveData(source_file="test.dat")
        save.account = PlayerAccount(player_name="Bob", level=5)
        dumped = save.model_dump()
        restored = SaveData.model_validate(dumped)
        assert restored.account.player_name == "Bob"
        assert restored.account.level == 5
