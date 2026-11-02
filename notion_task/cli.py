import argparse
from datetime import date, timedelta
import os
import sys
from notion_task.formatter import (
    format_day_log_page_payload,
    format_task_item_payload,
    format_to_markdown,
)
from notion_task.models import DailyPlan, TaskItem
from notion_task.notion_client import NotionClient


def prompt_text(label: str, default: str = "") -> str:
    prompt_str = f"{label} [{default}]: " if default else f"{label}: "
    val = input(prompt_str).strip()
    return val if val else default


def prompt_task_items(bucket_name: str, default_mode: str = "⚙️ Process", default_energy: str = "🔅 Medium") -> list[TaskItem]:
    print(f"\n--- {bucket_name} ---")
    print("(พิมพ์ชื่องาน แล้วกด Enter; กด Enter บรรทัดว่างเพื่อสิ้นสุดหมวดนี้)")
    items: list[TaskItem] = []
    while True:
        try:
            task_title = input("ชื่องาน: ").strip()
        except EOFError:
            break
        if not task_title:
            break

        time_block = input("  ช่วงเวลา (เช่น 14:30–15:45 หรือเว้นว่าง): ").strip()
        est_str = input("  ประเมินเวลา (นาที) [30]: ").strip()
        est_min = int(est_str) if est_str.isdigit() else 30

        print(f"  โหมด [1] 🧠 Immersive (โฟกัสลึก) หรือ [2] ⚙️ Process (งานย่อย/เอกสาร) [ค่าเริ่มต้น: {default_mode}]: ", end="")
        mode_in = input().strip()
        mode = "🧠 Immersive" if mode_in == "1" else ("⚙️ Process" if mode_in == "2" else default_mode)

        print("  หมวด PARA [1] 🎸 Teaching [2] ☁️ AWS [3] 🎬 Lecture [4] 🏠 Life [5] 🗂️ Admin [5]: ", end="")
        area_in = input().strip()
        area_map = {
            "1": "🎸 Teaching",
            "2": "☁️ AWS SAA",
            "3": "🎬 Chunnylab Lecture",
            "4": "🏠 Life",
            "5": "🗂️ Admin",
        }
        area = area_map.get(area_in, "🗂️ Admin")

        subtasks: list[str] = []
        sub_in = input("  Tasks ย่อย (คั่นด้วยจุลภาค ',' หรือเว้นว่าง): ").strip()
        if sub_in:
            subtasks = [s.strip() for s in sub_in.split(",") if s.strip()]

        items.append(
            TaskItem(
                task=task_title,
                bucket=bucket_name,
                energy=default_energy,
                mode=mode,
                area=area,
                time_block=time_block,
                est_minutes=est_min,
                subtasks=subtasks,
            )
        )
    return items


def run_interactive_intake() -> DailyPlan:
    print("=" * 60)
    print("  🎯 Daily Task Planner (Second Brain / PARA)")
    print("  แนวคิด: Plan → Execute → Wrap-Up (Ultimate Brain)")
    print("=" * 60)

    target_input = input("วางแผนสำหรับวันไหน? [1] วันนี้ (ค่าเริ่มต้น) หรือ [2] พรุ่งนี้: ").strip()
    if target_input == "2":
        plan_date = date.today() + timedelta(days=1)
    else:
        plan_date = date.today()

    print(f"\n[กำหนดวันที่: {plan_date.isoformat()}]")

    goal = prompt_text("1. เป้าหมายสำคัญที่สุดของวันนี้ (Daily Goal)")
    cutoff = prompt_text("2. กฎการตัดทิ้งหากเวลาไม่พอ (Cut-off Rule)")

    mit_list = prompt_task_items("🌟 Top Priorities (MIT)", default_mode="🧠 Immersive", default_energy="🔋 High")
    sec_list = prompt_task_items("📋 Secondary Tasks", default_mode="⚙️ Process", default_energy="🔅 Medium")
    qw_list = prompt_task_items("⚡ Quick Wins (< 15 นาที)", default_mode="⚙️ Process", default_energy="🪫 Low")

    notes = prompt_text("3. บันทึกหรือบริบทเพิ่มเติม (Notes)")

    all_tasks = mit_list + sec_list + qw_list
    total_est_hours = sum(t.est_minutes for t in all_tasks) / 60.0

    return DailyPlan(
        plan_date=plan_date,
        goal=goal,
        cutoff_rule=cutoff,
        tasks=all_tasks,
        notes=notes,
        focus_hours=round(total_est_hours, 1),
    )


def sync_plan_to_notion(plan: DailyPlan, client: NotionClient) -> None:
    logs_db_id = os.getenv("NOTION_LOGS_DB_ID", "")
    tasks_db_id = os.getenv("NOTION_TASKS_DB_ID", "")

    if not logs_db_id or not tasks_db_id:
        print("\n💡 หากต้องการซิงก์ตรงเข้า Notion Database กรุณากำหนด:")
        print("   - NOTION_LOGS_DB_ID (สำหรับ Daily Logs)")
        print("   - NOTION_TASKS_DB_ID (สำหรับ Daily Tasks)")
        print("   (ในไฟล์ .env หรือ Environment variable)")
        return

    print("\n⏳ กำลังสร้างหน้าวันใน Daily Logs...")
    day_payload = format_day_log_page_payload(plan, logs_db_id)
    day_res = client.create_page(day_payload)
    day_page_id = day_res.get("id", "")
    print(f"✅ บันทึกหน้าวันสำเร็จ: {day_res.get('url', day_page_id)}")

    date_str = plan.plan_date.isoformat()
    print(f"⏳ กำลังบันทึก {len(plan.tasks)} งานลง Daily Tasks database...")
    for t in plan.tasks:
        task_payload = format_task_item_payload(t, date_str, tasks_db_id, day_page_id)
        client.create_page(task_payload)
    print("🚀 ซิงก์ข้อมูลทั้งหมดเข้าสู่ Notion สำเร็จเรียบร้อย!")


def main() -> None:
    parser = argparse.ArgumentParser(description="Daily Task Planner (Second Brain PARA)")
    parser.add_argument("--sync", action="store_true", help="Sync plan to Notion database directly")
    parser.add_argument("--output", type=str, default="", help="Save Markdown to file path")
    args = parser.parse_args()

    plan = run_interactive_intake()
    md_content = format_to_markdown(plan)

    print("\n" + "=" * 60)
    print(f"  📋 สรุปแผนงานประจำวัน: {plan.title}")
    print("=" * 60)
    print(md_content)

    out_file = args.output or f"daily_plan_{plan.plan_date.isoformat()}.md"
    try:
        with open(out_file, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"💾 บันทึกไฟล์ Markdown ที่: {out_file}")
    except OSError as e:
        print(f"⚠️ ไม่สามารถบันทึกไฟล์: {e}", file=sys.stderr)

    if args.sync or (os.getenv("NOTION_API_KEY") and os.getenv("NOTION_TASKS_DB_ID")):
        try:
            client = NotionClient()
            sync_plan_to_notion(plan, client)
        except Exception as exc:
            print(f"❌ เกิดข้อผิดพลาดในการซิงก์ Notion: {exc}", file=sys.stderr)


if __name__ == "__main__":
    main()
