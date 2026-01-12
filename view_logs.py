import sqlite3

conn = sqlite3.connect("asha_sahayi.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM patient_visits")
rows = cursor.fetchall()

print("\n📋 ASHA Sahayi – Patient Visit Logs\n")
for row in rows:
    print(row)

conn.close()
