import sqlite3

# --- STANDALONE FUNCTIONS ---

def add_submissions(cursor, submissions_list):
    """Inserts a list of submissions into the database."""
    query = """
    INSERT INTO submissions (
        wsNum, problemName, problemPoints, andrewID, 
        originalCode, correctedCode, correctedIsCorrect, 
        partialCreditPct, partialCreditPoints, note
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    cursor.executemany(query, submissions_list)

def get_ws_credits_and_notes(cursor, ws_number):
    """
    Retrieves student IDs, points, and notes for a specific ws,
    only including entries that have been corrected.
    """
    query = """
        SELECT andrewID, partialCreditPoints, note 
        FROM submissions 
        WHERE wsNum = ? AND correctedCode IS NOT NULL
    """
    cursor.execute(query, (ws_number,))
    return cursor.fetchall()

# --- MAIN EXECUTION LOGIC ---

# 1. Connect to the writing session database
con = sqlite3.connect("ws.db")
cur = con.cursor()

# 2. Define the schema (note the removed trailing comma after 'note')
create_table_sql = """
CREATE TABLE IF NOT EXISTS submissions (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    wsNum               INTEGER NOT NULL,
    problemName         TEXT NOT NULL,
    problemPoints       INTEGER NOT NULL, 
    andrewID            TEXT NOT NULL,
    originalCode        TEXT NOT NULL,
    correctedCode       TEXT,
    correctedIsCorrect  INTEGER DEFAULT 0,
    partialCreditPct    REAL DEFAULT 0.0,
    partialCreditPoints REAL DEFAULT 0.0,
    note                TEXT DEFAULT ""
);
"""
cur.execute(create_table_sql)

# 3. Create indexes for performance
cur.execute("CREATE INDEX IF NOT EXISTS idx_andrewID ON submissions(andrewID);")
cur.execute("CREATE INDEX IF NOT EXISTS idx_wsNum ON submissions(wsNum);")

# 4. Prepare test data (including an uncorrected entry to test the filter)
# Format: (wsNum, probName, probPoints, andrewID, orig, corrected, isCorr, pct, pts, note)
test_data = [
    (1, 'Loop Logic', 10, 'eochis', 'for i in range(10)', 'for i in range(10):', 1, 1.0, 10.0, "Perfect syntax."),
    (1, 'Loop Logic', 10, 'truannec', 'for i in range(5)', None, 0, 0.0, 0.0, "Pending review"),
    (1, 'Printing', 5, 'elenali', 'print "hello"', 'print("hello")', 1, 1.0, 5.0, "Corrected legacy syntax."),
    (2, 'Functions', 20, 'karancha', 'def add(a,b):', 'def add(a,b): pass', 0, 0.5, 10.0, "Incomplete function.")
]

add_submissions(cur, test_data)
con.commit()

# 5. Display results for Writing Session 1
print(f"Results for Writing Session 1 (Corrected Only):")
print(f"{'Student':<12} | {'Score':<6} | {'Notes'}")
print("-" * 45)

session_results = get_ws_credits_and_notes(cur, 1)
for row in session_results:
    # row[0]=andrewID, row[1]=partialCreditPoints, row[2]=note
    print(f"{row[0]:<12} | {row[1]:<6} | {row[2]}")

# 6. Cleanup
cur.close()
con.close()