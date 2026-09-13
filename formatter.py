"""
Intelligent Presentation Formatter for IPL (Intelligent Programming Language / Aether).
Renders tables, bar charts, sentiment cards, confidence badges, gauges, cards, trees, and JSON using Rich.
"""
import json
from typing import Any, Dict, List, Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.syntax import Syntax


class IntelligentFormatter:
    def __init__(self, console: Optional[Console] = None):
        self.console = console or Console()

    def render_format(self, value: Any, format_style: str, raw_ivalue=None, title_override: Optional[str] = None):
        fmt = format_style.lower().strip()

        if fmt == "table":
            self.render_table(value, title_override)
        elif fmt in ("bar_chart", "chart", "bars"):
            self.render_bar_chart(value, title_override)
        elif fmt in ("badge", "status"):
            self.render_badge(value, raw_ivalue)
        elif fmt in ("sentiment", "mood"):
            self.render_sentiment(value)
        elif fmt in ("gauge", "meter", "progress"):
            self.render_gauge(value, raw_ivalue, title_override)
        elif fmt in ("card", "panel"):
            self.render_card(value, raw_ivalue, title_override)
        elif fmt == "tree":
            self.render_tree(value, title_override)
        elif fmt == "json":
            self.render_json(value)
        else:
            self.console.print(f"[{fmt.upper()}] {value}")

    def render_table(self, data: Any, title: Optional[str] = None):
        """Renders lists of dicts, records, or key-values as a clean terminal table."""
        table_title = title or "📊 Intelligent Data Table"
        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
            headers = list(data[0].keys())
            table = Table(title=table_title, show_header=True, header_style="bold cyan")
            for h in headers:
                table.add_column(str(h).capitalize())
            for row in data:
                table.add_row(*[str(row.get(h, "")) for h in headers])
            self.console.print(table)
        elif isinstance(data, dict):
            table = Table(title=table_title, show_header=True, header_style="bold magenta")
            table.add_column("Property", style="bold cyan")
            table.add_column("Value", style="green")
            for k, v in data.items():
                table.add_row(str(k), str(v))
            self.console.print(table)
        elif isinstance(data, list):
            table = Table(title=table_title, show_header=True, header_style="bold blue")
            table.add_column("Index", justify="right", style="dim")
            table.add_column("Item")
            for idx, item in enumerate(data):
                table.add_row(str(idx), str(item))
            self.console.print(table)
        else:
            self.console.print(f"[bold yellow]Cannot render type '{type(data).__name__}' as table.[/bold yellow] Value: {data}")

    def render_bar_chart(self, data: Any, title: Optional[str] = None):
        """Renders numeric dictionaries or lists as proportional Unicode bar charts."""
        items = []
        if isinstance(data, dict):
            # If intent distribution
            if "distribution" in data and isinstance(data["distribution"], dict):
                items = list(data["distribution"].items())
            else:
                items = list(data.items())
        elif isinstance(data, list):
            items = [(f"Item {i}", v) for i, v in enumerate(data)]

        if not items:
            self.console.print("[dim](Empty chart data)[/dim]")
            return

        numeric_items = []
        for k, v in items:
            try:
                numeric_items.append((str(k), float(v)))
            except (ValueError, TypeError):
                pass

        if not numeric_items:
            self.console.print(f"[bold red]Data has no numeric fields for bar chart:[/bold red] {data}")
            return

        max_val = max(v for _, v in numeric_items) or 1.0
        max_label_len = max(len(k) for k, _ in numeric_items)
        max_bar_width = 28

        chart_lines = []
        for label, val in numeric_items:
            ratio = max(0.0, min(1.0, val / max_val))
            filled = int(round(ratio * max_bar_width))
            empty = max_bar_width - filled
            bar = f"[cyan]{'█' * filled}[/cyan][dim]{'░' * empty}[/dim]"
            val_str = f"{val:.2f}" if isinstance(val, float) and val < 1.0 else f"{val:,.1f}"
            chart_lines.append(f" {label.ljust(max_label_len)}  [{bar}] [bold green]{val_str}[/bold green]")

        panel = Panel(
            "\n".join(chart_lines),
            title=title or "📈 [bold]Intelligent Proportional Distribution[/bold]",
            border_style="bright_blue"
        )
        self.console.print(panel)

    def render_badge(self, value: Any, raw_ivalue=None):
        """Renders an intelligent confidence status badge."""
        confidence = raw_ivalue.confidence if raw_ivalue else 0.95
        pct = int(confidence * 100)
        filled = int(confidence * 10)
        empty = 10 - filled
        meter = f"[{'■' * filled}{'□' * empty}]"

        color = "green" if confidence >= 0.85 else ("yellow" if confidence >= 0.70 else "red")

        val_str = str(value)
        if isinstance(value, dict) and "formatted" in value:
            val_str = value["formatted"]
        elif isinstance(value, dict) and "summary" in value:
            val_str = value["summary"]

        text = Text()
        text.append(" STATUS: ", style="bold")
        text.append(f"{val_str} ", style="bold white")
        text.append(f"| CONFIDENCE: {pct}% ", style=f"bold {color}")
        text.append(meter, style=color)

        panel = Panel(text, border_style=color, expand=False)
        self.console.print(panel)

    def render_sentiment(self, data: Any):
        """Renders emotional valence and sentiment telemetry."""
        if isinstance(data, dict) and "score" in data:
            score = data["score"]
            label = data.get("label", "Unknown")
            conf = data.get("confidence", 0.9)
            color = "green" if score > 0.1 else ("red" if score < -0.1 else "yellow")
            icon = "🟢" if score > 0.1 else ("🔴" if score < -0.1 else "🟡")

            # Valence visual bar [-1.0 to +1.0]
            val_norm = (score + 1.0) / 2.0  # 0.0 to 1.0
            ticks = 20
            pos = int(round(val_norm * (ticks - 1)))
            meter_chars = ["─"] * ticks
            meter_chars[pos] = "◆"
            meter_str = "".join(meter_chars)

            content = (
                f"{icon} [bold {color}]{label.upper()}[/bold {color}]\n"
                f"  • Valence Spectrum : [{meter_str}] {score:+.3f}\n"
                f"  • Posterior Conf   : [bold]{conf*100:.0f}%[/bold]\n"
                f"  • Summary          : {data.get('summary', '')}"
            )
            self.console.print(Panel(content, title="🧠 [bold]Sentiment Neural Vector[/bold]", border_style=color))
        else:
            self.console.print(f"[dim]Sentiment:[/dim] {data}")

    def render_gauge(self, data: Any, raw_ivalue=None, title: Optional[str] = None):
        """Renders a progress/utilization gauge."""
        val = 0.0
        if isinstance(data, (int, float)):
            val = float(data)
        elif isinstance(data, dict):
            if "value" in data:
                val = float(data["value"])
            elif "score" in data:
                val = float(data["score"]) * 100
            elif "amount" in data:
                val = float(data["amount"])

        # Determine percentage or cap
        pct = max(0.0, min(100.0, val if val <= 100.0 else (val % 100)))
        total_slots = 24
        filled = int(round((pct / 100.0) * total_slots))
        empty = total_slots - filled
        color = "green" if pct < 70 else ("yellow" if pct < 90 else "red")

        bar = f"[{color}]{'█' * filled}[/{color}][dim]{'░' * empty}[/dim]"
        gauge_text = f"  [{bar}] [bold {color}]{pct:.1f}%[/bold {color}]"

        panel = Panel(
            gauge_text,
            title=title or "🎛️ [bold]System Metric Gauge[/bold]",
            border_style=color,
            expand=False
        )
        self.console.print(panel)

    def render_card(self, data: Any, raw_ivalue=None, title: Optional[str] = None):
        """Renders an executive/presentation card."""
        card_title = title or "📋 [bold]Intelligent Insight Card[/bold]"
        lines = []

        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, dict):
                    lines.append(f"  • [bold cyan]{k}[/bold cyan]: {json.dumps(v)}")
                else:
                    lines.append(f"  • [bold cyan]{k}[/bold cyan]: [white]{v}[/white]")
        elif isinstance(data, list):
            for idx, item in enumerate(data[:6]):
                lines.append(f"  [{idx+1}] {item}")
        else:
            lines.append(f"  {str(data)}")

        if raw_ivalue and raw_ivalue.confidence:
            conf_pct = int(raw_ivalue.confidence * 100)
            lines.append(f"\n[dim]Model Confidence: {conf_pct}% | Formal Membrane Verified[/dim]")

        panel = Panel("\n".join(lines), title=card_title, border_style="cyan", padding=(1, 2))
        self.console.print(panel)

    def render_tree(self, data: Any, title: Optional[str] = None):
        """Renders hierarchical data as a Rich Tree."""
        tree = Tree(title or "🌳 [bold]Hierarchical Structure[/bold]")

        def add_nodes(parent_node, obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, (dict, list)):
                        branch = parent_node.add(f"[bold cyan]{k}[/bold cyan]")
                        add_nodes(branch, v)
                    else:
                        parent_node.add(f"[bold cyan]{k}[/bold cyan]: [green]{v}[/green]")
            elif isinstance(obj, list):
                for idx, item in enumerate(obj):
                    if isinstance(item, (dict, list)):
                        branch = parent_node.add(f"[dim]#[/dim][bold blue]{idx}[/bold blue]")
                        add_nodes(branch, item)
                    else:
                        parent_node.add(f"[dim]#[/dim][bold blue]{idx}[/bold blue]: {item}")
            else:
                parent_node.add(str(obj))

        add_nodes(tree, data)
        self.console.print(tree)

    def render_json(self, data: Any):
        """Pretty-prints JSON with syntax coloring."""
        try:
            formatted = json.dumps(data, indent=2, default=str)
            syntax = Syntax(formatted, "json", theme="monokai", line_numbers=False)
            self.console.print(syntax)
        except Exception as e:
            self.console.print(f"[red]JSON formatting error:[/red] {e}")
