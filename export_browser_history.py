import sqlite3
import csv
import os
import shutil
import datetime
from pathlib import Path
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Export Arc browser history within a specified date range.")
    parser.add_argument("--start", type=int, help="Start date: 0 for today, -1 for yesterday, etc.")
    parser.add_argument("--end", type=int, help="End date: same format as start.")
    return parser.parse_args()

def get_date_range(start, end):
    # Get the current date in the local timezone
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if start is None and end is None:
        # If no arguments are provided, set range to current day
        start_date = today
        end_date = today.replace(hour=23, minute=59, second=59)
    else:
        # If arguments are provided, set the specified range
        start = start or 0  # Use 0 (today) if start is not specified
        end = end or 0  # Use 0 (today) if end is not specified
        start_date = today + datetime.timedelta(days=start)
        end_date = (today + datetime.timedelta(days=end)).replace(hour=23, minute=59, second=59)
    return start_date, end_date

def get_arc_history(start_date, end_date):
    history_path = Path.home() / "Library/Application Support/Arc/User Data/Default/History"
    
    print(f"Checking for history file at: {history_path}")
    if not history_path.exists():
        raise FileNotFoundError(f"Arc history file not found at {history_path}")
    
    desktop_path = Path.home() / "Desktop"
    temp_path = desktop_path / "TempArcHistory"
    shutil.copy2(history_path, temp_path)
    print(f"Copied history to temporary file: {temp_path}")
    
    conn = sqlite3.connect(temp_path)
    cursor = conn.cursor()
    
    query = """
    SELECT 
        urls.id, 
        datetime(visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime') AS visit_time, 
        urls.title, 
        urls.url 
    FROM visits 
    LEFT JOIN urls ON visits.url = urls.id 
    WHERE datetime(visits.visit_time/1000000-11644473600, 'unixepoch', 'localtime') BETWEEN ? AND ?
    ORDER BY visits.visit_time DESC
    """
    
    print("Executing SQL query...")
    cursor.execute(query, (start_date.strftime("%Y-%m-%d %H:%M:%S"), end_date.strftime("%Y-%m-%d %H:%M:%S")))
    history = cursor.fetchall()
    print(f"Fetched {len(history)} rows from the database")
    
    conn.close()
    os.remove(temp_path)
    print("Temporary file deleted")
    
    return history

def save_to_csv(history, start_date, end_date):
    desktop_path = Path.home() / "Desktop"
    csv_path = desktop_path / f"arc_history_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}.csv"
    
    print(f"Saving history to CSV file: {csv_path}")
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['ID', 'Visit Time', 'Title', 'URL'])
        writer.writerows(history)
    
    print(f"History saved to {csv_path}")
    print(f"Number of rows written: {len(history)}")

def main():
    try:
        args = parse_arguments()
        start_date, end_date = get_date_range(args.start, args.end)
        print(f"Fetching history from {start_date} to {end_date}")
        
        history = get_arc_history(start_date, end_date)
        if not history:
            print(f"No history data found between {start_date} and {end_date}.")
        else:
            save_to_csv(history, start_date, end_date)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()