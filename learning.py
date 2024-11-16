import json
import sqlite3
import os

DB_FILE = "learning.db"
RULES_FILE = "rules.json"

# Initialize SQLite DB
def initialize_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rules (
            selector TEXT PRIMARY KEY,
            rule TEXT
        )
    """)
    conn.commit()
    conn.close()

# Load rules from JSON
def load_rules_from_json():
    if not os.path.exists(RULES_FILE):
        return {}
    with open(RULES_FILE, "r") as f:
        return json.load(f)

# Save rules to JSON
def save_rules_to_json(rules):
    with open(RULES_FILE, "w") as f:
        json.dump(rules, f, indent=4)

# Get rule from JSON or SQLite
def get_rule(selector):
    # Load rules from JSON
    rules = load_rules_from_json()
    if selector in rules:
        return rules[selector]
    
    # Fallback to SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT rule FROM rules WHERE selector = ?", (selector,))
    result = cursor.fetchone()
    conn.close()
    return json.loads(result[0]) if result else None

# Save rule to JSON and SQLite
def save_rule(selector, rule):
    # Save to JSON
    rules = load_rules_from_json()
    rules[selector] = rule
    save_rules_to_json(rules)
    
    # Save to SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR REPLACE INTO rules (selector, rule) VALUES (?, ?)",
        (selector, json.dumps(rule))
    )
    conn.commit()
    conn.close()
