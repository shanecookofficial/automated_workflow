import sqlite3

def get_all_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [table[0] for table in cursor.fetchall()]

def display_table_contents(cursor, table_name):
    print(f"\nContents of table '{table_name}':")
    cursor.execute(f"SELECT * FROM {table_name}")
    columns = [description[0] for description in cursor.description]
    print(", ".join(columns))  # Print column names
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No data found.")

def main():
    # Connect to the SQLite database
    conn = sqlite3.connect('tcg_database.db')
    cursor = conn.cursor()
    
    # Get all table names
    table_names = get_all_table_names(cursor)
    print("Tables in the database:", ", ".join(table_names))
    
    # Display contents of each table
    for table_name in table_names:
        display_table_contents(cursor, table_name)
    
    # Close the connection to the database
    conn.close()

if __name__ == "__main__":
    main()
