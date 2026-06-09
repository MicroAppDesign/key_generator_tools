# key_generator_tools

🛡️ Secure Key & Password Generator (CSPRNG)

เครื่องมือเว็บแอปพลิเคชันสำหรับสร้างคีย์เข้ารหัสและรหัสผ่านปลอดภัยแบบ client-side 100% โดยใช้ Web Crypto API ของเบราว์เซอร์เพื่อสร้างค่าความสุ่มจากฮาร์ดแวร์จริง ทำงานได้ทั้งออนไลน์และออฟไลน์

## จุดเด่น

- สร้างคีย์และรหัสผ่านด้วย window.crypto.getRandomValues
- ทำงานแบบ Zero-Server / Zero-Trust โดยไม่มีการส่งข้อมูลไปเซิร์ฟเวอร์
- แสดงค่า Entropy / Security Metrics แบบ real-time
- รองรับ QR Code แบบออฟไลน์ด้วย QRious
- ใช้ Tailwind CSS v4 และ dependency ภายในโปรเจกต์เพื่อให้เปิดใช้งานแบบ offline ได้จริง

## วิธีรัน

1. ติดตั้ง dependency
   ```bash
   npm install
   ```
2. build CSS แบบ offline
   ```bash
   npm run build:css
   ```
3. เปิดหน้าเว็บด้วยเซิร์ฟเวอร์ท้องถิ่น
   ```bash
   python3 -m http.server 3000
   ```
4. เปิดในเบราว์เซอร์
   ```text
   http://127.0.0.1:3000/
   ```

## โครงสร้างโปรเจกต์

- index.html — หน้าแอปหลัก
- src/input.css — ไฟล์ Tailwind v4 entry
- styles/tailwind.css — CSS ที่ build แล้วสำหรับใช้งาน offline
- node_modules/ — dependency ภายในโปรเจกต์

## ข้อควรทราบ

- แนะนำให้เปิดผ่าน localhost หรือ http.server เพื่อให้ asset โหลดได้ถูกต้อง
- หากต้องการใช้งานในเครื่องที่ไม่มีอินเทอร์เน็ต ให้ทำการติดตั้ง dependency ก่อนแล้วค่อยเปิดใช้งานแบบออฟไลน์

## สิทธิ์การใช้งาน

ซอฟต์แวร์นี้เป็น Public Domain คุณสามารถดัดแปลง ใช้งาน คัดลอก หรือแจกจ่ายต่อได้อย่างเสรี
