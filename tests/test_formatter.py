import unittest
from datetime import date
from notion_task.formatter import format_to_markdown, format_to_notion_blocks
from notion_task.models import DailyPlan


class TestDailyPlanFormatter(unittest.TestCase):
    def test_markdown_formatting(self):
        plan = DailyPlan(
            plan_date=date(2026, 11, 2),
            priorities=["Deploy backend", "Review PR"],
            secondary_tasks=["Update docs"],
            quick_wins=["Pay electric bill"],
            notes="Focus block in morning",
        )
        md = format_to_markdown(plan)
        self.assertIn("## ⚡ Focus Plan: 2026-11-02", md)
        self.assertIn("- [ ] **Deploy backend**", md)
        self.assertIn("- [ ] **Review PR**", md)
        self.assertIn("- [ ] Update docs", md)
        self.assertIn("- [ ] Pay electric bill", md)
        self.assertIn("Focus block in morning", md)

    def test_notion_blocks_conversion(self):
        plan = DailyPlan(
            plan_date=date(2026, 11, 2),
            priorities=["Deep Work Task"],
            secondary_tasks=["Minor Task"],
            quick_wins=["Quick Call"],
        )
        blocks = format_to_notion_blocks(plan)
        self.assertTrue(len(blocks) > 0)
        types = [b["type"] for b in blocks]
        self.assertIn("heading_2", types)
        self.assertIn("to_do", types)
        self.assertIn("divider", types)


if __name__ == "__main__":
    unittest.main()
