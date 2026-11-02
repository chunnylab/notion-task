# Notion Task: Daily Task Planner (Second Brain / PARA)

ระบบวางแผนและแตกย่อยงานรายวัน (Daily Task Planning System) เชื่อมต่อ Notion โดยจัดวางไว้ในหมวด **Projects** ตามแนวคิด Second Brain (PARA Method: Projects, Areas, Resources, Archives) ของ Tiago Forte

ออกแบบด้วยหลักการ **Single-Page Command Center (หน้าเดียวจบ ไม่แยกหน้าย่อย)** เพื่อขจัดปัญหาความยุ่งยากในการคลิกเปิดหน้าย่อย (Sublinks / Subpages) โดยใช้ระบบ Checkbox คู่กับ **Toggle** สำหรับกางดูและพับเก็บขั้นตอนย่อย (Micro-tasks) ได้ในหน้าเดียว

---

## จุดเด่น (Features)

- **Single-Page Command Center:** รวมทุกอย่างไว้ในหน้าหลักหน้าเดียว เห็นเป้าหมาย งานสำคัญ ตารางเวลา และรายละเอียดปลีกย่อยได้ทันทีโดยไม่ต้องคลิกเปิดหน้าย่อย
- **Toggle-Based Micro-Tasks:** แสดงชื่องานหลักเป็น Checkbox บนหน้าหลัก และซ่อนขั้นตอนย่อย (20-45 นาที) ไว้ใน `<toggle>` ใต้งานนั้น เพื่อรักษาความสะอาดของหน้าจอแต่ยังคงความละเอียดไว้ครบถ้วน
- **Second Brain PARA Alignment:** วางโครงสร้าง Daily Planner ไว้ในหมวด Projects เชื่อมโยงงานรายวันเข้ากับเป้าหมายที่แท้จริง
- **AI-Powered Intake Interview:** สัมภาษณ์คัดกรอง 4 ประเด็นสำคัญ (Hard Deadlines, Deep Work, พลังงานและเวลา, Quick Wins) ก่อนเริ่มลงมือ
- **Mode Tagging:** แยกงานแบบ Immersive (ต้องมีสมาธิต่อเนื่อง ห้ามรบกวน) ออกจากงาน Process (งานย่อย/เอกสาร/ธุระ)
- **Zero-Dependency CLI:** โปรแกรม Python ขนาดกะทัดรัดที่ใช้เฉพาะ Python Standard Library ใช้งานได้ทันทีโดยไม่ต้องติดตั้งแพ็กเกจภายนอก
- **Notion Integration:** รองรับทั้งการอัปเดตผ่าน Notion MCP บน AI Assistant และการซิงก์ผ่าน Notion API ตรง
- **Safe & Public-Ready:** ตั้งค่า `.gitignore` คลุมไฟล์ Credential, Token, `.env` และข้อมูลส่วนบุคคลอย่างรัดกุม

---

## โครงสร้างหน้าควบคุม (Single-Page Structure)

```
[ Daily Task Planner Hub ]
├── Callout: เป้าหมายประจำวัน (Goal) & กฎการตัดทิ้ง (Cut-off Rule)
├── รายการงานสำคัญอันดับ 1–3 (Most Important Tasks - MIT)
│   ├── [ ] 1. ชื่องานหลัก [ช่วงเวลา] (พลังงาน | โหมด)
│   │   └── ▶ Toggle: ขั้นตอนย่อย (Micro-tasks เช็กลิสต์)
│   ├── [ ] 2. ชื่องานหลัก [ช่วงเวลา] (พลังงาน | โหมด)
│   │   └── ▶ Toggle: ขั้นตอนย่อย (Micro-tasks เช็กลิสต์)
│   └── [ ] 3. ชื่องานหลัก [ช่วงเวลา] (พลังงาน | โหมด)
│       └── ▶ Toggle: ขั้นตอนย่อย (Micro-tasks เช็กลิสต์)
├── รายการงานรอง (Secondary Tasks)
├── รายการงานสั้น (Quick Wins < 15 นาที)
├── ▶ Toggle: ตารางเวลาประจำวัน (Time Blocking Table)
├── ▶ Toggle: กลยุทธ์และเทคนิคเฉพาะโปรเจกต์
├── ▶ Toggle: สรุปผลงานตอนเย็น (Evening Wrap-Up)
├── ▶ Toggle: คลังประวัติวันย้อนหลัง (Past Archives)
└── ▶ Toggle: แม่แบบคำสั่ง AI สำหรับวางแผนรายวัน (Prompts)
```

---

## การเลือกโมเดล (Model Selection: จัดการเอง หรือ AI สลับให้?)

**คำตอบ:** ผู้ใช้จำเป็นต้องเลือกสลับโมเดลผ่านเมนูตัวเลือกโมเดล (Dropdown) ในหน้าต่างแชตด้วยตนเอง เนื่องจากระบบความปลอดภัยและส่วนต่อประสาน (UI) ของแชตไม่อนุญาตให้ AI สลับโมเดลของห้องสนทนาโดยอัตโนมัติ

### คำแนะนำขั้นตอนการทำงาน (Recommended Workflow):
1. **ขั้นตอนคุยข้อมูลเบื้องต้น (Fast Intake):**
   - ใช้โมเดลที่ตอบสนองไว (เช่น Gemini Flash หรือ Claude Sonnet) คุยตอบคำถามสั้นๆ เพื่อระบุรายการสิ่งที่ต้องทำในวันนี้
2. **ขั้นตอนแตกย่อยงานซับซ้อน (Deep Breakdown with Opus):**
   - เมื่อมีงานซับซ้อน งานที่มีเงื่อนไขเกี่ยวพันหลายฝ่าย หรือวันที่ตารางแน่นมาก ให้สลับโมเดลเป็น **Claude Opus**
   - ใช้คำสั่งจากไฟล์ [`prompts/02_opus_deep_planner_prompt.md`](prompts/02_opus_deep_planner_prompt.md) เพื่อให้ Opus วิเคราะห์ Dependency, คำนวณ Buffer และจัด Energy Allocation อย่างละเอียด
3. **ขั้นตอนบันทึกขึ้น Notion (Execution):**
   - ให้ AI บันทึกหรืออัปเดตหน้า Notion ด้วยโครงสร้าง Checkbox + Toggle ได้ทันที

---

## โครงสร้างโปรเจกต์ (Repository Structure)

```
notion-task/
├── .env.example                  # ตัวอย่างการตั้งค่า Environment variables
├── .gitignore                    # ป้องกัน Token และ Secret รั่วไหล
├── LICENSE                       # MIT License
├── README.md                     # เอกสารแนะนำและคู่มือการใช้งาน
├── plan.py                       # สคริปต์รัน CLI หลัก
├── prompts/                      # แม่แบบ Prompt สำหรับใช้งานประจำวัน
│   ├── 01_daily_intake_prompt.md       # คำสั่งสัมภาษณ์คัดกรองงานรายวัน
│   ├── 02_opus_deep_planner_prompt.md  # คำสั่งวางแผนเชิงลึกสำหรับ Opus
│   └── 03_evening_review_prompt.md     # คำสั่งสรุปงานตอนเย็นและยกยอดไปวันพรุ่งนี้
├── skills/
│   └── daily-planner/
│       └── SKILL.md              # สกิลสำหรับติดตั้งใน Antigravity / Claude
├── notion_task/                  # Python Package (Standard Library)
│   ├── __init__.py
│   ├── cli.py                   # ตัวควบคุม Interactive CLI
│   ├── formatter.py             # จัดรูปแบบ Single-Page Markdown และ Toggles
│   ├── models.py                # โครงสร้างข้อมูล TaskItem และ DailyPlan
│   └── notion_client.py         # ไคลเอนต์เรียก Notion API (Zero dependencies)
└── tests/
    └── test_formatter.py        # ชุดทดสอบ Unit test
```

---

## วิธีใช้งาน (Getting Started)

### วิธีที่ 1: ใช้งานผ่าน AI Assistant (Prompt / Skill)
1. เปิด AI Assistant ที่คุณใช้งาน (เช่น Antigravity, Claude, ChatGPT)
2. คัดลอกเนื้อหาจาก [`prompts/01_daily_intake_prompt.md`](prompts/01_daily_intake_prompt.md) ไปวาง
3. ตอบคำถาม 4 ข้อที่ AI สัมภาษณ์
4. เมื่อได้แผนงาน ให้นำไปวางใน Notion หรือสั่ง AI อัปเดตหน้า `Daily Task Planner` โดยตรง

### วิธีที่ 2: ใช้งานผ่าน Terminal (CLI)

รันโปรแกรมสัมภาษณ์ในเครื่องของคุณ:

```bash
# รันโหมดสัมภาษณ์และบันทึกเป็น Markdown
python3 plan.py

# กำหนดชื่อไฟล์ผลลัพธ์
python3 plan.py --output my_plan.md
```

---

## การทดสอบ (Testing)

โปรเจกต์นี้มาพร้อมชุดทดสอบ Unit test:

```bash
python3 -m unittest discover -s tests
```

---

## ความปลอดภัย (Security)

- ไฟล์ `.env`, คีย์ API, และ Token ต่างๆ ถูกละเว้นผ่าน `.gitignore` ไม่ให้ถูกส่งเข้า Git Repository
- ไม่มีข้อมูล Token หรือสิทธิ์ลับใดๆ ถูกฮาร์ดโค้ดลงในซอร์สโค้ด

---

## ลิขสิทธิ์ (License)

โปรเจกต์นี้เผยแพร่ภายใต้ [MIT License](LICENSE) สามารถนำไปใช้งาน ปรับแต่ง และแชร์ต่อได้อย่างอิสระ
