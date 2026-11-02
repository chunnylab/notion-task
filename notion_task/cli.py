import argparse
from datetime import date, timedelta
import os
import sys
from notion_task.formatter import format_to_markdown, format_to_notion_blocks
from notion_task.models import DailyPlan
from notion_task.notion_client import NotionClient


def prompt_multiline(question: str) -> list[str]:
    print(f"\n{question} (ป้อนแต่ละรายการแล้วกด Enter, กด Enter บรรทัดว่างเพื่อสิ้นสุด):")
    items = []
    while True:
        try:
            line = input("> ").strip()
        except EOFError:
            break
        if not line:
            break
        items.append(line)
    return items


def run_interactive_intake() -> DailyPlan:
    print("=" * 60)
    print("  🎯 Daily Task Planner (Second Brain / PARA)")
    print("=" * 60)

    target_input = input("วางแผนสำหรับวันไหน? [1] วันนี้ (ค่าเริ่มต้น) หรือ [2] พรุ่งนี้: ").strip()
    if target_input == "2":
        plan_date = date.today() + timedelta(days=1)
    else:
        plan_date = date.today()

    print(f"\n[กำหนดวันที่: {plan_date.isoformat()}]")

    priorities = prompt_multiline("1. Top Priorities / MIT (งานสำคัญ 1-3 งานที่ต้องส่งหรือสร้างผลลัพธ์สูง)")
    secondary = prompt_multiline("2. Secondary Tasks (งานรองที่ทำได้ถ้างานหลักเสร็จก่อน)")
    quick_wins = prompt_multiline("3. Quick Wins (งานสั้นๆ ไม่เกิน 15 นาที เช่น โทรศัพท์ จ่ายบิล ซื้อของ)")

    print("\n4. บันทึกเพิ่มเติม หรือบริบทพิเศษ (กด Enter เพื่อข้าม):")
    notes = input("> ").strip()

    return DailyPlan(
        plan_date=plan_date,
        priorities=priorities,
        secondary_tasks=secondary,
        quick_wins=quick_wins,
        notes=notes,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily Task Planner (Second Brain PARA)")
    parser.add_argument("--sync", action="store_true", help="Sync plan to Notion page directly")
    parser.add_argument("--page-id", type=str, default="", help="Target Notion page ID to append plan")
    parser.add_argument("--output", type=str, default="", help="Save Markdown to file path")
    args = parser.parse_args()

    plan = run_interactive_intake()
    md_content = format_to_markdown(plan)

    print("\n" + "=" * 60)
    print("  📋 สรุปแผนงานประจำวัน")
    print("=" * 60)
    print(md_content)

    out_file = args.output or f"daily_plan_{plan.plan_date.isoformat()}.md"
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"💾 บันทึกไฟล์ Markdown ที่: {out_file}")
    except OSError as e:
        print(f"⚠️ ไม่สามารถบันทึกไฟล์: {e}", file=sys.stderr)

    if args.sync or os.getenv("NOTION_API_KEY"):
        page_id = args.page_id or os.getenv("NOTION_DAILY_TASK_PAGE_ID", "")
        if not page_id:
            print("\n💡 หากต้องการซิงก์ขึ้น Notion อัตโนมัติ ให้กำหนด NOTION_DAILY_TASK_PAGE_ID ใน .env หรือส่งผ่าน --page-id")
            return

        try:
            client = NotionClient()
            blocks = format_to_notion_blocks(plan)
            client.append_block_children(page_id, blocks)
            print("🚀 ซิงก์ข้อมูลขึ้น Notion สำเร็จ!")
        except Exception as exc:
            print(f"❌ เกิดข้อผิดพลาดในการซิงก์ Notion: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
