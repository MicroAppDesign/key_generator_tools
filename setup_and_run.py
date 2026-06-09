#!/usr/bin/env python3
"""
สคริปต์ Python สำหรับการ Setup และรันโปรเจกต์ key_generator_tools อัตโนมัติ (Tailwind CSS v4)
ช่วยลดขั้นตอนที่ซ้ำซ้อน ติดตั้ง Dependencies และรันทั้งการ Watch CSS และเปิด HTTP Server ไปพร้อมกัน
"""

import os
import sys
import json
import subprocess
import threading
import time

# กำหนดค่าตัวแปรเบื้องต้นสำหรับโปรเจกต์
PORT = 3000
INPUT_CSS_PATH = "input.css"
OUTPUT_CSS_PATH = "styles/output.css"

def print_step(message):
    """ฟังก์ชันเสริมสำหรับแสดงข้อความสถานะแต่ละขั้นตอนให้ชัดเจนใน Terminal"""
    print(f"\n\033[94m[STEP]\033[0m {message}")

def print_success(message):
    """ฟังก์ชันเสริมสำหรับแสดงสถานะที่ทำงานสำเร็จ"""
    print(f"\033[92m[SUCCESS]\033[0m {message}")

def print_error(message):
    """ฟังก์ชันเสริมสำหรับแสดงสถานะเมื่อเกิดข้อผิดพลาด"""
    print(f"\033[91m[ERROR]\033[0m {message}", file=sys.stderr)

def check_node_environment():
    """ขั้นตอนที่ 1: ตรวจสอบความพร้อมของ Node.js และ Node Package Manager (npm)"""
    print_step("กำลังตรวจสอบสภาพแวดล้อม (Node.js & npm)...")
    try:
        # ตรวจสอบเวอร์ชันของ Node.js (ใช้ -v ตัวเดียวก็เพียงพอ ลดความซ้ำซ้อนในการรันสองคำสั่ง)
        node_version = subprocess.check_output(["node", "-v"], text=True).strip()
        # ตรวจสอบเวอร์ชันของ npm
        npm_version = subprocess.check_output(["npm", "--version"], text=True).strip()
        
        print(f"  - Node.js Version: {node_version}")
        print(f"  - npm Version: {npm_version}")
    except FileNotFoundError:
        print_error("ไม่พบ Node.js หรือ npm ในเครื่องนี้! กรุณาติดตั้งก่อนรันสคริปต์นี้")
        sys.exit(1)

def init_project_files():
    """ขั้นตอนที่ 2: สร้างและเตรียมโครงสร้างไฟล์ที่ถูกต้อง (อิงตามมาตรฐาน Tailwind v4)"""
    print_step("กำลังสร้างไฟล์โครงสร้างสำหรับโปรเจกต์...")

    # 2.1 สร้าง package.json ถ้ายังไม่มี โดยกำหนดค่าเริ่มต้นและสคริปต์สำหรับรัน
    if not os.path.exists("package.json"):
        package_data = {
            "name": "key_generator_tools",
            "version": "1.0.0",
            "description": "Tools for generating secure keys with Tailwind CSS v4",
            "main": "index.html",
            "type": "module",
            "scripts": {
                # สคริปต์สำหรับคอมไพล์ CSS ด้วย Tailwind v4 CLI
                "build": f"tailwindcss -i {INPUT_CSS_PATH} -o {OUTPUT_CSS_PATH}",
                "dev": f"tailwindcss -i {INPUT_CSS_PATH} -o {OUTPUT_CSS_PATH} --watch"
            }
        }
        with open("package.json", "w", encoding="utf-8") as f:
            json.dump(package_data, f, indent=2, ensure_ascii=False)
        print("  - สร้างไฟล์ package.json เรียบร้อยแล้ว")
    else:
        print("  - พบไฟล์ package.json อยู่แล้ว (ข้ามการสร้างใหม่)")

    # 2.2 สร้าง input.css สำหรับ Tailwind v4 (ใช้แค่บรรทัดเดียว ไม่จำเป็นต้องพึ่งไฟล์ config)
    if not os.path.exists(INPUT_CSS_PATH):
        with open(INPUT_CSS_PATH, "w", encoding="utf-8") as f:
            f.write('@import "tailwindcss";\n')
        print(f"  - สร้างไฟล์ {INPUT_CSS_PATH} ด้วยโค้ดนำเข้าของ Tailwind v4 เรียบร้อยแล้ว")
    else:
        print(f"  - พบไฟล์ {INPUT_CSS_PATH} อยู่แล้ว (ข้ามการสร้างใหม่)")

    # 2.3 ตรวจสอบและสร้างโฟลเดอร์ปลายทางสำหรับเก็บไฟล์ output.css
    os.makedirs(os.path.dirname(OUTPUT_CSS_PATH), exist_ok=True)

    # 2.4 สร้างไฟล์ .gitignore เพื่อป้องกันไม่ให้โฟลเดอร์ติดตั้ง/ไฟล์ชยะถูกส่งขึ้น Git
    if not os.path.exists(".gitignore"):
        gitignore_content = """node_modules/
styles/
.DS_Store
*.log
"""
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print("  - สร้างไฟล์ .gitignore เรียบร้อยแล้ว")
    else:
        print("  - พบไฟล์ .gitignore อยู่แล้ว (ข้ามการสร้างใหม่)")

    # 2.5 สร้างหน้าตัวอย่าง index.html เพื่อใช้ในการทดสอบระบบและเรียกใช้งาน CSS
    if not os.path.exists("index.html"):
        html_content = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Key Generator Tools (Tailwind v4)</title>
    <!-- ลิงก์ไปยัง CSS ที่ผ่านการคอมไพล์แล้วจากโฟลเดอร์ styles -->
    <link rel="stylesheet" href="styles/output.css">
</head>
<body class="bg-slate-900 text-white flex flex-col items-center justify-center min-h-screen font-sans">
    <div class="bg-slate-800 p-8 rounded-2xl shadow-xl max-w-md w-full border border-slate-700">
        <h1 class="text-3xl font-bold mb-4 text-emerald-400">Key Generator Tools</h1>
        <p class="text-slate-300 mb-6">ยินดีด้วย! สภาพแวดล้อมโปรเจกต์ของคุณรันได้เป็นปกติด้วย Tailwind CSS v4</p>
        <button class="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-semibold px-6 py-3 rounded-xl transition duration-200 w-full shadow-lg">
            สร้างคีย์ใหม่
        </button>
    </div>
</body>
</html>
"""
        with open("index.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        print("  - สร้างหน้าตัวอย่าง index.html เรียบร้อยแล้ว")

def install_dependencies():
    """ขั้นตอนที่ 3: ติดตั้ง Tailwind v4 และ CLI เครื่องมือที่เกี่ยวข้องลงในโปรเจกต์"""
    print_step("กำลังติดตั้ง Dependencies (Tailwind CSS v4 & @tailwindcss/cli)...")
    try:
        # สั่งติดตั้งแบบระบุเวอร์ชัน 4.1.7 ตามที่ต้องการในโหมดพัฒนา
        subprocess.run(
            ["npm", "install", "tailwindcss@^4.1.7", "@tailwindcss/cli@^4.1.7"], 
            check=True
        )
        print_success("ติดตั้งเครื่องมือ Tailwind CSS v4 สำเร็จแล้ว!")
    except subprocess.CalledProcessError as e:
        print_error(f"การติดตั้งล้มเหลว: {e}")
        sys.exit(1)

def run_tailwind_watch():
    """ฟังก์ชันที่สองสำหรับรันกระบวนการ Tailwind CSS Watch (รันในพื้นหลังผ่าน Thread)"""
    print("\n\033[95m[Tailwind CLI]\033[0m กำลังเริ่มต้นระบบเฝ้าดูการทำงานของ CSS (Watch Mode)...")
    try:
        # เรียกใช้สคริปต์คอมไพล์ CSS ที่เขียนไว้ใน package.json
        subprocess.run(["npm", "run", "dev"], check=True)
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดในการรัน Tailwind CLI: {e}")

def run_python_server():
    """ฟังก์ชันหลักสำหรับเริ่มรัน Local Web Server ด้วย Python เพื่อดูผลงานทางบราวเซอร์"""
    print(f"\n\033[96m[Python Server]\033[0m กำลังรัน Local HTTP Server ที่ พอร์ต {PORT}...")
    try:
        # รันเว็บเซิร์ฟเวอร์ของ Python บนพอร์ตที่ระบุ
        subprocess.run([sys.executable, "-m", "http.server", str(PORT)], check=True)
    except KeyboardInterrupt:
        print_success("\nหยุดการรันระบบโดยผู้ใช้แล้ว")
    except Exception as e:
        print_error(f"เกิดข้อผิดพลาดในการรัน HTTP Server: {e}")

if __name__ == "__main__":
    # รันขั้นตอนตรวจสภาพแวดล้อม
    check_node_environment()
    
    # รันขั้นตอนจัดโครงสร้างไฟล์
    init_project_files()
    
    # รันขั้นตอนติดตั้งเครื่องมือสำหรับ Tailwind v4
    install_dependencies()
    
    # การแก้ปัญหาเรื่องการ "บล็อก" (Block) Terminal ของคำสั่งรัน Server:
    # โดยเราจะแยกตัว Tailwind CLI --watch ไปรันบนเบื้องหลัง (Background Thread)
    # เพื่อให้ Terminal หน้าจอนี้สามารถแสดงผลทั้งการ Build CSS และมีเซิร์ฟเวอร์รันขนานกันได้
    tailwind_thread = threading.Thread(target=run_tailwind_watch, daemon=True)
    tailwind_thread.start()
    
    # ปล่อยให้เวลา Tailwind รันและสร้างหน้า CSS ด่านแรก 2 วินาที ก่อนที่เว็บเซิร์ฟเวอร์จะเปิด
    time.sleep(2)
    
    # เริ่มต้นรันเซิร์ฟเวอร์ Python เป็นหน้าต่างหลัก
    run_python_server()
```
eof

### คำอธิบายความสามารถและจุดที่แก้ไขความซ้ำซ้อนในสคริปต์นี้:

1. **สืบทอดเวอร์ชันตามความต้องการของคุณจริง**: สคริปต์ทำการติดตั้ง `"tailwindcss": "^4.1.7"` และ `"@tailwindcss/cli": "^4.1.7"` โดยตรง และกำหนดให้เป็นมาตรฐานใน `package.json`
2. **ไม่สร้างไฟล์ config ที่ล้าสมัย**: ตัวสคริปต์ข้ามขั้นตอนการสร้าง `tailwind.config.js` ไปอย่างสิ้นเชิง เนื่องจาก v4 มีตัวสแกนอัตโนมัติภายในตัว และใช้เพียงไฟล์ CSS หลักในการทำหน้าที่ทั้งหมด
3. **ลดขั้นตอนเช็ก Environment ซ้ำซ้อน**: เปลี่ยนจากการรัน `npm --version` และ `node --version` สองรอบ มาเป็นการรันตรวจสอบแบบกระชับในฟังก์ชันเดียว
4. **แก้ปัญหา Terminal ถูกล็อก (Block)**: สคริปต์นี้ใช้ประโยชน์จาก `threading` ของ Python ในการแยกรันคำสั่ง `npm run dev` (เพื่อเฝ้าดูคลาสของ CSS ตัวใหม่ๆ แล้วอัปเดตแบบ Realtime) ไว้ที่ Background Thread จากนั้นรันเว็บเซิร์ฟเวอร์ของ Python ในตัวหลัก ทำให้เรา**ไม่ต้องเปิดหน้าต่าง Terminal หลายจอ**เพื่อรัน 2 คำสั่งพร้อมกันอีกต่อไป

### วิธีใช้งานสคริปต์นี้:
1. นำโค้ดด้านบนไปเซฟไว้ที่ไฟล์ชื่อ `setup_and_run.py` ภายในโฟลเดอร์ `/workspaces/key_generator_tools`
2. เปิด Terminal และสั่งรันไฟล์ด้วยคำสั่ง:
   ```bash
   python3 setup_and_run.py