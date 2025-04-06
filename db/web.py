import sqlite3

DB_PATH = "news_aggregator.db"

def remove_invalid_websites():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Delete websites that have no news items
    cursor.execute("""
        DELETE FROM websites
        WHERE id NOT IN (
            SELECT DISTINCT website_id FROM news
        );
    """)
    
    conn.commit()
    conn.close()
    print("Removed invalid websites from the database.")

if __name__ == "__main__":
    remove_invalid_websites()
