import sqlite3

conn = sqlite3.connect("devops_agent.db")
cursor = conn.cursor()

print("===== INCIDENTS TABLE =====\n")

cursor.execute("PRAGMA table_info(incidents)")

for row in cursor.fetchall():
    print(row)