#!/usr/bin/env python3
"""Check the backup-test log and report whether a restore test is due.

Reads backup-log-template.csv (or a CSV path given as the first argument),
finds the most recent test, and prints a reminder if the next test is overdue
or the last result was a failure. Standard library only. No network access.
"""
import csv
import sys
from datetime import date, datetime

path = sys.argv[1] if len(sys.argv) > 1 else "backup-log-template.csv"

with open(path, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

if not rows:
    print("No restore tests logged yet. Run a restore test now.")
    sys.exit(1)

last = max(rows, key=lambda r: r["date_tested"])
due = datetime.strptime(last["next_test_due"], "%Y-%m-%d").date()
today = date.today()
status = 0

if last["result"].strip().lower() != "pass":
    print(f"ALERT: last restore test on {last['date_tested']} did not pass. Notify the incident lead.")
    status = 1
if today > due:
    print(f"REMINDER: restore test was due on {due}. Test restoring 3 files from the offsite copy.")
    status = 1
if status == 0:
    print(f"OK: last test {last['date_tested']} passed; next test due {due}.")
sys.exit(status)
