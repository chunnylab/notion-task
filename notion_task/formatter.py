from typing import Any, Dict, List
from notion_task.models import DailyPlan


def format_to_markdown(plan: DailyPlan) -> str:
    """Format a DailyPlan into Notion-compatible Markdown."""
    date_str = plan.plan_date.isoformat()
    lines = [
        f"## ⚡ Focus Plan: {date_str}",
        "",
        "### 🌟 Top Priorities (MIT)",
    ]
    if plan.priorities:
        for p in plan.priorities:
            lines.append(f"- [ ] **{p}**")
    else:
        lines.append("- [ ] ")

    lines.append("")
    lines.append("### 📋 Secondary Tasks")
    if plan.secondary_tasks:
        for t in plan.secondary_tasks:
            lines.append(f"- [ ] {t}")
    else:
        lines.append("- [ ] ")

    lines.append("")
    lines.append("### ⚡ Quick Wins (< 15 min)")
    if plan.quick_wins:
        for q in plan.quick_wins:
            lines.append(f"- [ ] {q}")
    else:
        lines.append("- [ ] ")

    if plan.notes:
        lines.append("")
        lines.append("### 📝 Notes & Context")
        lines.append(plan.notes)

    lines.append("")
    return "\n".join(lines)


def format_to_notion_blocks(plan: DailyPlan) -> List[Dict[str, Any]]:
    """Convert DailyPlan to Notion API block objects for appending."""
    date_str = plan.plan_date.isoformat()
    blocks: List[Dict[str, Any]] = [
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": f"⚡ Focus Plan: {date_str}"}}]
            },
        },
        {
            "object": "block",
            "type": "heading_3",
            "heading_3": {
                "rich_text": [{"type": "text", "text": {"content": "🌟 Top Priorities (MIT)"}}]
            },
        },
    ]

    for p in plan.priorities:
        blocks.append({
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": p}, "annotations": {"bold": True}}],
                "checked": False,
            },
        })

    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "📋 Secondary Tasks"}}]
        },
    })
    for t in plan.secondary_tasks:
        blocks.append({
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": t}}],
                "checked": False,
            },
        })

    blocks.append({
        "object": "block",
        "type": "heading_3",
        "heading_3": {
            "rich_text": [{"type": "text", "text": {"content": "⚡ Quick Wins (< 15 min)"}}]
        },
    })
    for q in plan.quick_wins:
        blocks.append({
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [{"type": "text", "text": {"content": q}}],
                "checked": False,
            },
        })

    if plan.notes:
        blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [{"type": "text", "text": {"content": plan.notes}}],
                "icon": {"type": "emoji", "emoji": "📝"},
            },
        })

    blocks.append({"object": "block", "type": "divider", "divider": {}})
    return blocks
