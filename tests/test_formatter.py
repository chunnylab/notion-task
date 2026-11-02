import unittest
from datetime import date
from notion_task.formatter import (
    format_day_log_page_payload,
    format_task_item_payload,
    format_to_markdown,
)
from notion_task.models import DailyPlan, TaskItem


class TestDailyPlanFormatter(unittest.TestCase):
    def test_markdown_formatting(self):
        plan = DailyPlan(
            plan_date=date(2026, 11, 2),
            goal="เคลียร์งานสำคัญและเรียนจบ 1 บท",
            cutoff_rule="ถ้าเกิน 18:00 เลื่อนงานรอง",
            tasks=[
                TaskItem(
                    task="Deploy backend",
                    bucket="🌟 MIT",
                    energy="🔋 High",
                    mode="🧠 Immersive",
                    time_block="10:00–12:00",
                    subtasks=["Check db connection", "Run migrations"],
                ),
                TaskItem(
                    task="Update docs",
                    bucket="📋 Secondary",
                    energy="🔅 Medium",
                    mode="⚙️ Process",
                ),
                TaskItem(
                    task="Pay bills",
                    bucket="⚡ Quick Win",
                    energy="🪫 Low",
                    mode="⚙️ Process",
                    est_minutes=10,
                ),
            ],
            notes="Morning coffee focus",
        )
        md = format_to_markdown(plan)
        self.assertIn("Deploy backend", md)
        self.assertIn("Check db connection", md)
        self.assertIn("Update docs", md)
        self.assertIn("Pay bills", md)
        self.assertIn("เป้าหมายหลัก (Daily Goal):", md)
        self.assertIn("Cut-off Rule", md)

    def test_day_log_payload_structure(self):
        plan = DailyPlan(
            plan_date=date(2026, 11, 2),
            goal="Complete AWS module",
            tasks=[],
        )
        payload = format_day_log_page_payload(plan, "12345678-1234-1234-1234-123456789abc")
        self.assertEqual(payload["parent"]["database_id"], "12345678123412341234123456789abc")
        self.assertIn("Day", payload["properties"])
        self.assertIn("Date", payload["properties"])
        self.assertIn("Phase", payload["properties"])
        self.assertEqual(payload["properties"]["Date"]["date"]["start"], "2026-11-02")

    def test_task_item_payload_structure(self):
        task = TaskItem(
            task="Write unit tests",
            bucket="🌟 MIT",
            energy="🔋 High",
            mode="🧠 Immersive",
            area="☁️ AWS SAA",
            time_block="14:00–15:00",
            est_minutes=60,
            subtasks=["Test A", "Test B"],
        )
        payload = format_task_item_payload(
            task,
            plan_date="2026-11-02",
            database_id="db-uuid",
            day_page_id="day-uuid",
        )
        self.assertEqual(payload["parent"]["database_id"], "dbuuid")
        self.assertEqual(payload["properties"]["Task"]["title"][0]["text"]["content"], "Write unit tests")
        self.assertEqual(payload["properties"]["Bucket"]["select"]["name"], "🌟 MIT")
        self.assertEqual(payload["properties"]["Mode"]["select"]["name"], "🧠 Immersive")
        self.assertEqual(payload["properties"]["Day"]["relation"][0]["id"], "dayuuid")
        self.assertEqual(len(payload["children"]), 2)


if __name__ == "__main__":
    unittest.main()
