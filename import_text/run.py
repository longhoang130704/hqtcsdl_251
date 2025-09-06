import pandas as pd
import psycopg2

# 1. Đọc file Excel
file_path = r"D:/HCMUT-K22/HQTCSDL/btl/data/Radiologists Report.xlsx"
df = pd.read_excel(file_path)

# Đổi tên cột để dễ xử lý
df.columns = ["patient_id", "note"]

# 2. Kết nối PostgreSQL
conn = psycopg2.connect(
    dbname="postgres",
    user="postgres",
    password="12345678",
    host="localhost",
    port="5433"
)
cur = conn.cursor()

# 3. Insert dữ liệu
for _, row in df.iterrows():
    note_value = "" if pd.isna(row["note"]) else str(row["note"])
    cur.execute("""
        INSERT INTO patient (patient_id, note)
        VALUES (%s, %s)
        ON CONFLICT (patient_id) DO UPDATE
        SET note = EXCLUDED.note;
    """, (int(row["patient_id"]), row["note"]))

# 4. Commit và đóng kết nối
conn.commit()
cur.close()
conn.close()

print("✅ Import dữ liệu thành công!")
