"""Base report interface - all report types must implement this protocol."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path

from tower_analyzer.models.save_data import SaveData


@dataclass
class ReportContext:
    """Context passed to every report generator."""

    save: SaveData
    output_path: Path | None = None
    extra: dict[str, object] = field(default_factory=dict)


class BaseReport(ABC):
    """Abstract base class for all report generators.

    Subclasses must implement :meth:`generate`, which receives a
    :class:`ReportContext` and returns report content as a string.

    Future report types:
        - EconomyReport
        - WorkshopReport
        - LabsReport
        - CardsReport
        - ModulesReport
        - ROIReport
        - RecommendationsReport
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable name for this report."""
        ...

    @abstractmethod
    def generate(self, ctx: ReportContext) -> str:
        """Generate the report and return it as a string.

        Parameters
        ----------
        ctx:
            Report context containing parsed save data and optional output path.

        Returns
        -------
        str
            Report content (Markdown by default).
        """
        ...

    def write(self, ctx: ReportContext, path: Path) -> None:
        """Generate the report and write it to *path*.

        Parameters
        ----------
        ctx:
            Report context.
        path:
            Output file path.
        """
        content = self.generate(ctx)
        path.write_text(content, encoding="utf-8")
