from typing import Any, Dict, List
from notion_task.models import DailyPlan, TaskItem


def format_single_page_markdown(plan: DailyPlan) -> str:
    """Format a DailyPlan into Notion single-page layout with collapsible toggles."""
    date_str = plan.plan_date.isoformat()
    lines = [
        f"## แผนงานประจำวัน: {plan.title} ({date_str})",
        "",
    ]

    if plan.goal or plan.cutoff_rule:
        lines.append("> **เป้าหมายหลัก (Daily Goal):** " + (plan.goal or "-"))
        if plan.cutoff_rule:
            lines.append("> **กฎการตัดทิ้ง (Cut-off Rule):** " + plan.cutoff_rule)
        lines.append("")

    lines.append("### งานสำคัญอันดับ 1–3 (Most Important Tasks - MIT)")
    if plan.mit_tasks:
        for idx, t in enumerate(plan.mit_tasks, 1):
            time_part = f" [{t.time_block}]" if t.time_block else ""
            mode_energy = f" (ระดับพลังงาน: {t.energy} | โหมด: {t.mode})"
            lines.append(f"- [ ] **{idx}. {t.task}**{time_part}{mode_energy}")
            if t.subtasks:
                lines.append("    <toggle>")
                lines.append("    <b>Tasks</b>")
                for sub in t.subtasks:
                    lines.append(f"    - [ ] {sub}")
                lines.append("    </toggle>")
    else:
        lines.append("- [ ] ")

    lines.append("")
    lines.append("### งานรอง (Secondary Tasks)")
    if plan.secondary_tasks:
        for t in plan.secondary_tasks:
            time_part = f" [{t.time_block}]" if t.time_block else ""
            lines.append(f"- [ ] {t.task}{time_part} ({t.energy})")
            if t.subtasks:
                lines.append("    <toggle>")
                lines.append("    <b>Tasks</b>")
                for sub in t.subtasks:
                    lines.append(f"    - [ ] {sub}")
                lines.append("    </toggle>")
    else:
        lines.append("- [ ] ")

    lines.append("")
    lines.append("### งานสั้น (Quick Wins: น้อยกว่า 15 นาที)")
    if plan.quick_wins:
        for t in plan.quick_wins:
            lines.append(f"- [ ] {t.task} ({t.est_minutes} นาที)")
    else:
        lines.append("- [ ] ")

    if plan.notes:
        lines.extend([
            "",
            "### บันทึกเพิ่มเติม (Notes & Context)",
            plan.notes,
        ])

    lines.append("")
    return "\n".join(lines)


def format_to_markdown(plan: DailyPlan) -> str:
    """Standard markdown formatter for terminal and text file output."""
    return format_single_page_markdown(plan)


def format_day_log_page_payload(plan: DailyPlan, database_id: str) -> Dict[str, Any]:
    """Build payload for creating a new Day Log page in the Daily Logs database."""
    date_str = plan.plan_date.isoformat()
    clean_db_id = database_id.replace("-", "")

    content_blocks: List[Dict[str, Any]] = []

    if plan.goal:
        content_blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"เป้าหมายวันนี้: {plan.goal}", "link": None}}
                ],
                "icon": {"type": "emoji", "emoji": "🧭"},
                "color": "blue_background",
            },
        })

    if plan.cutoff_rule:
        content_blocks.append({
            "object": "block",
            "type": "callout",
            "callout": {
                "rich_text": [
                    {"type": "text", "text": {"content": f"Cut-off Rule: {plan.cutoff_rule}", "link": None}}
                ],
                "icon": {"type": "emoji", "emoji": "✂️"},
                "color": "red_background",
            },
        })

    content_blocks.extend([
        {
            "object": "block",
            "type": "heading_2",
            "heading_2": {
                "rich_text": [{"type": "text", "text": {"content": "🌙 Wrap-Up"}}]
            },
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "ทำอะไรสำเร็จบ้าง (Wins)"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": ""}}]},
                    }
                ],
            },
        },
        {
            "object": "block",
            "type": "toggle",
            "toggle": {
                "rich_text": [{"type": "text", "text": {"content": "งานที่ค้าง: Roll over / Backlog / Drop"}}],
                "children": [
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": [{"type": "text", "text": {"content": ""}}]},
                    }
                ],
            },
        },
    ])

    return {
        "parent": {"database_id": clean_db_id},
        "icon": {"type": "emoji", "emoji": "🌤️"},
        "properties": {
            "Day": {
                "title": [{"type": "text", "text": {"content": plan.title}}]
            },
            "Date": {
                "date": {"start": date_str}
            },
            "Phase": {
                "status": {"name": "Executing"}
            },
            "Energy": {
                "select": {"name": plan.energy}
            },
            "Focus Hours": {
                "number": plan.focus_hours if plan.focus_hours > 0 else None
            },
        },
        "children": content_blocks,
    }


def format_task_item_payload(task: TaskItem, plan_date: str, database_id: str, day_page_id: str = "") -> Dict[str, Any]:
    """Build payload for creating a task page inside the Daily Tasks database."""
    clean_db_id = database_id.replace("-", "")
    properties: Dict[str, Any] = {
        "Task": {
            "title": [{"type": "text", "text": {"content": task.task}}]
        },
        "Date": {
            "date": {"start": plan_date}
        },
        "Status": {
            "status": {"name": task.status}
        },
        "Bucket": {
            "select": {"name": task.bucket}
        },
        "Energy": {
            "select": {"name": task.energy}
        },
        "Mode": {
            "select": {"name": task.mode}
        },
        "Area": {
            "select": {"name": task.area}
        },
        "Est (min)": {
            "number": task.est_minutes
        },
    }

    if task.time_block:
        properties["Time Block"] = {
            "rich_text": [{"type": "text", "text": {"content": task.time_block}}]
        }

    if day_page_id:
        clean_day_id = day_page_id.replace("-", "")
        properties["Day"] = {
            "relation": [{"id": clean_day_id}]
        }

    children: List[Dict[str, Any]] = []
    if task.subtasks:
        for sub in task.subtasks:
            children.append({
                "object": "block",
                "type": "to_do",
                "to_do": {
                    "rich_text": [{"type": "text", "text": {"content": sub}}],
                    "checked": False,
                },
            })

    payload: Dict[str, Any] = {
        "parent": {"database_id": clean_db_id},
        "properties": properties,
    }
    if children:
        payload["children"] = children

    return payload
