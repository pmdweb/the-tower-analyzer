"""MarkdownReport - top-level Markdown summary report."""

from __future__ import annotations

from datetime import UTC, datetime

from tower_analyzer.reports.base import BaseReport, ReportContext


class MarkdownReport(BaseReport):
    """Generate a Markdown summary report of a parsed save file.

    Future sections (not yet implemented):
        - Economy analysis
        - Workshop ROI
        - Labs ROI
        - Cards analysis
        - Module recommendations
    """

    @property
    def name(self) -> str:
        return "Summary Report"

    def generate(self, ctx: ReportContext) -> str:
        """Generate a Markdown summary report.

        Parameters
        ----------
        ctx:
            Report context.

        Returns
        -------
        str
            Markdown content.
        """
        save = ctx.save
        account = save.account
        now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")

        lines = [
            "# The Tower Save Analyzer - Summary Report",
            "",
            f"*Generated: {now}*  ",
            f"*Source file: `{save.source_file}`*  ",
            f"*File size: {save.raw_bytes_size:,} bytes*",
            "",
            "---",
            "",
            "## Player Account",
            "",
            "| Field | Value |",
            "|-------|-------|",
            f"| Name | {account.player_name or '*(unknown)*'} |",
            f"| Level | {account.level} |",
            f"| Prestige | {account.prestige} |",
            f"| Highest Wave | {account.highest_wave} |",
            f"| Coins | {account.coins:,.0f} |",
            f"| Gems | {account.gems:,} |",
            f"| Game Version | {account.game_version or '*(unknown)*'} |",
            "",
            "---",
            "",
            "## Workshop",
            "",
            f"*{len(save.workshop.upgrades)} upgrades parsed.*",
            "",
            "> ⚠️ Workshop detail requires complete BinaryFormatter decoding.",
            "",
            "---",
            "",
            "## Labs",
            "",
            f"*{len(save.labs.upgrades)} research upgrades parsed.*",
            "",
            "> ⚠️ Labs detail requires complete BinaryFormatter decoding.",
            "",
            "---",
            "",
            "## Cards",
            "",
            f"*{len(save.cards.cards)} cards parsed.*",
            "",
            "> ⚠️ Cards detail requires complete BinaryFormatter decoding.",
            "",
            "---",
            "",
            "## Economy",
            "",
            "| Resource | Amount |",
            "|----------|--------|",
            f"| Coins | {save.economy.coins:,.0f} |",
            f"| Gems | {save.economy.gems:,} |",
            f"| Keys | {save.economy.keys:,} |",
            f"| Dust | {save.economy.dust:,} |",
            f"| Orbs | {save.economy.orbs:,} |",
            "",
            "---",
            "",
            "## Statistics",
            "",
            "| Stat | Value |",
            "|------|-------|",
            f"| Total Games Played | {save.statistics.total_games_played:,} |",
            f"| Total Kills | {save.statistics.total_kills:,} |",
            f"| Highest Wave Ever | {save.statistics.highest_wave_ever:,} |",
            f"| Total Playtime | {save.statistics.total_playtime_seconds / 3600:.1f} h |",
            "",
            "---",
            "",
        ]

        if save.parse_warnings:
            lines += [
                "## Parse Warnings",
                "",
            ]
            for warning in save.parse_warnings:
                lines.append(f"- ⚠️ {warning}")
            lines.append("")

        return "\n".join(lines)
