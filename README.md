# Notion Task: Daily Task Planner (Second Brain / PARA)

ระบบวางแผนและแตกย่อยงานรายวัน (Daily Task Planning System) เชื่อมต่อ Notion โดยจัดวางไว้ในหมวด **Projects** ตามแนวคิด Second Brain (PARA Method: Projects, Areas, Resources, Archives) ของ Tiago Forte ผสานกระบวนการทำงานระดับพรีเมียม Plan, Execute, Wrap-Up (PEW) จาก Ultimate Brain

ออกแบบมาเพื่อให้ทุกคนสามารถวางแผนงานประจำวันได้อย่างรวดเร็ว แปลงเป้าหมายใหญ่เป็น Micro-tasks ที่ทำได้จริง พร้อมระบบสัมภาษณ์คัดกรองลำดับความสำคัญ โหมดการทำงาน (Immersive vs Process) และการจับคู่ระดับพลังงาน

---

## จุดเด่น (Features)

- **Second Brain PARA Alignment:** วางโครงสร้าง Daily Planner ไว้ในหมวด Projects เชื่อมโยงงานรายวันเข้ากับเป้าหมายที่แท้จริง
- **2-Database Architecture:**
  - `Daily Tasks`: จัดการงานรายชิ้น พร้อมสถานะ (To Do, Doing, Done, Dropped), Bucket (MIT, Secondary, Quick Win), โหมด (Immersive vs Process), และระดับพลังงาน
  - `Daily Logs`: บันทึกหน้าประจำวัน (One page per day) มี Rollup คำนวณความคืบหน้า (%) อัตโนมัติจากงานที่ผูกไว้ พร้อมพื้นที่จด Wins และสรุปผล
- **Interactive Multi-view Dashboard:**
  - Board: แสดง Today tasks ตามสถานะ To Do, Doing, Done
  - Board by Energy: แยกกลุ่มงานตามพลังงานที่ต้องใช้ (High, Medium, Low)
  - Gallery: คลังประวัติวันย้อนหลัง พร้อมแถบความคืบหน้าและคะแนนประเมิน
  - Calendar: ปฏิทินรายเดือนแสดงความต่อเนื่องของงาน
- **AI-Powered Intake Interview:** สัมภาษณ์คัดกรอง 4 ประเด็นสำคัญ (Hard Deadlines, Deep Work, พลังงานและเวลา, Quick Wins) ก่อนเริ่มลงมือ
- **Mode Tagging:** แยกงานแบบ Immersive (ต้องมีสมาธิต่อเนื่อง ห้ามรบกวน) ออกจากงาน Process (งานย่อย/เอกสาร/ธุระ)
- **Zero-Dependency CLI:** โปรแกรม Python ขนาดกะทัดรัดที่ใช้เฉพาะ Python Standard Library ใช้งานได้ทันทีโดยไม่ต้องติดตั้งแพ็กเกจภายนอก
- **Notion Integration:** รองรับทั้งการบันทึกผ่าน Notion MCP บน AI Assistant และการซิงก์ผ่าน Notion API ตรงเข้าฐานข้อมูล
- **Safe & Public-Ready:** ตั้งค่า `.gitignore` คลุมไฟล์ Credential, Token, `.env` และข้อมูลส่วนบุคคลอย่างรัดกุม

---

## สถาปัตยกรรมฐานข้อมูล (Database Architecture)

ระบบประกอบด้วย 2 ฐานข้อมูลที่เชื่อมโยงกันแบบ Relation:

```
[ Daily Logs Database ]  <==== Two-way Relation ====>  [ Daily Tasks Database ]
  - Day (Title)                                           - Task (Title)
  - Date (Date)                                           - Status (To Do / Doing / Done / Dropped)
  - Phase (Planned / Executing / Reviewed)                - Date (Date)
  - Energy (High / Medium / Low)                          - Bucket (MIT / Secondary / Quick Win)
  - Progress (Rollup % from Tasks)                        - Mode (Immersive / Process)
  - Focus Hours (Number)                                  - Energy (High / Medium / Low)
  - Rating (1-5 Stars)                                    - Area (Teaching / AWS / Lecture / Life / Admin)
  - Wins (Text)                                           - Time Block (Text)
                                                          - Est min (Number)
                                                          - Day (Relation to Daily Logs)
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
   - ให้ AI บันทึกหน้าวันและงานทั้งหมดลง Notion ผ่าน Notion MCP หรือสั่งรันสคริปต์ CLI

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
│   ├── formatter.py             # จัดรูปแบบ Markdown และ Notion API Blocks/Payloads
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
4. เมื่อได้แผนงาน ให้นำไปวางใน Notion หรือหากใช้ Notion MCP ให้สั่ง AI บันทึกลงหน้า `Daily Task Planner` หรือฐานข้อมูลที่เกี่ยวข้องได้ทันที

### วิธีที่ 2: ใช้งานผ่าน Terminal (CLI)

รันโปรแกรมสัมภาษณ์ในเครื่องของคุณ:

```bash
# รันโหมดสัมภาษณ์และบันทึกเป็น Markdown
python3 plan.py

# กำหนดชื่อไฟล์ผลลัพธ์
python3 plan.py --output my_plan.md
```

### วิธีที่ 3: ซิงก์ขึ้น Notion API โดยตรงผ่าน CLI

1. คัดลอกไฟล์ `.env.example` เป็น `.env`:
   ```bash
   cp .env.example .env
   ```
2. ใส่ `NOTION_API_KEY` (จาก https://www.notion.so/my-integrations)
3. ใส่ `NOTION_LOGS_DB_ID` และ `NOTION_TASKS_DB_ID`
4. สั่งรันพร้อมส่งข้อมูลขึ้น Notion:
   ```bash
   python3 plan.py --sync
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
