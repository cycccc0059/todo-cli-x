# ----------------------------------------
# 🧰 Utils Module for Todo CLI X
# Contains reusable helpers for printing messages and formatting output.
# ----------------------------------------

from typing import List
from .core import TaskDict

# ANSI color codes for priority display
PRIORITY_COLORS = {
    "high": "\033[91m",     # red
    "medium": "\033[93m",   # yellow
    "low": "\033[0m",       # default
}
RESET = "\033[0m"


# -------------------------------
# 🎨 Message display utility
# -------------------------------

def print_message(kind: str, message: str) -> None:
    """
    Print a message with a contextual icon prefix.
    Supported kinds: success, delete, error, warning, info
    """
    icons = {
        "success": "✅",
        "delete": "🗑️",
        "error": "❌",
        "warning": "⚠️",
        "info": "ℹ️",
    }
    prefix = icons.get(kind, "")
    print(f"{prefix}  {message.lstrip()}")  # Extra space for better UX


# -------------------------------
# 📋 Task table formatter
# -------------------------------

def format_task_table(tasks: List[TaskDict], verbose: bool = False) -> str:
    """
    Return a formatted string displaying tasks in a table layout.
    Columns: ID | Status | Priority | Task | Due [| Created | Tags]
    """
    if not tasks:
        return "⚠️  No tasks to display."

    headers = ["ID", "Status", "Priority", "Task", "Due"]
    if verbose:
        headers.extend(["Created", "Tags"])

    rows: List[List[str]] = []
    for task in tasks:
        done = "✓" if task["done"] else "✗"
        priority = task["priority"]
        colored_priority = f"{PRIORITY_COLORS.get(priority, '')}{priority}{RESET}"
        row: List[str] = [
            str(task["id"]),
            done,
            colored_priority,
            task["text"],
            task.get("due") or ""
        ]
        if verbose:
            row.append(task.get("created", ""))  # fallback for retrocompatibility
            tags = task.get("tags")
            tags_str = ", ".join(tags) if tags else ""
            row.append(tags_str)
        rows.append(row)

    # Determine column widths
    columns = list(zip(*([headers] + rows)))
    col_widths: List[int] = [max(len(str(cell)) for cell in col) for col in columns]

    # Build table lines
    table_lines: List[str] = []

    header_line = "  ".join(h.ljust(w) for h, w in zip(headers, col_widths))
    table_lines.append(header_line)

    separator = "  ".join("─" * w for w in col_widths)
    table_lines.append(separator)

    for row in rows:
        line = "  ".join(str(cell).ljust(w) for cell, w in zip(row, col_widths))
        table_lines.append(line)

    return "\n".join(table_lines)

# -------------------------------
# 📊 Task summary printer
# -------------------------------

def print_task_summary(tasks: List[TaskDict]) -> None:
    """
    Print a summary of task statistics: total, completed, and remaining.
    """
    total = len(tasks)
    done = sum(1 for t in tasks if t["done"])
    left = total - done
    plural = "s" if total != 1 else ""

    if total == 0:
        print_message("info", "No tasks available.")
        return

    # Spacing for readability
    print()
    print_message("info", f"{total} task{plural} — {done} completed, {left} remaining")