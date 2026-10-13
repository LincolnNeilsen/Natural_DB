"""Natural-language question bot for the books database.

Flow: question -> GPT writes SQL -> run SQL on books.db -> GPT writes plain-English answer.
Usage: python db_bot.py [zero_shot|few_shot]
"""
import json
import os
import re
import sqlite3
import sys

from openai import OpenAI

MODEL = "gpt-4o-mini"
HERE = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(HERE, "books.db")
CONFIG_PATH = os.path.join(HERE, "config.json")

# Two prompting strategies. zero_shot gives only the schema; few_shot adds examples.
EXAMPLES = (
    "Examples:\n"
    "Q: How many books does Brandon Sanderson have?\n"
    "SQL: SELECT COUNT(*) FROM book_to_author ba JOIN Author a ON a.id = ba.author_id "
    "WHERE a.last_name = 'Sanderson';\n"
    "Q: Which publisher has the highest average rating?\n"
    "SQL: SELECT p.name FROM Publisher p JOIN Book b ON b.publisher_id = p.id "
    "JOIN Review r ON r.id = b.review_id GROUP BY p.id ORDER BY AVG(r.rating) DESC LIMIT 1;\n"
)
STRATEGIES = {
    "zero_shot": "",
    "few_shot": EXAMPLES,
}


def build_db():
    # ponytail: rebuild from scratch each run so the mock data is always known-good
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = sqlite3.connect(DB_PATH)
    for name in ("setup.sql", "setupData.sql"):
        with open(os.path.join(HERE, name), encoding="utf-8") as f:
            conn.executescript(f.read())
    conn.commit()
    conn.close()


def load_schema():
    with open(os.path.join(HERE, "setup.sql"), encoding="utf-8") as f:
        return f.read()


def ask_gpt(client, system, user):
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=0,
    )
    return resp.choices[0].message.content.strip()


def make_sql(client, question, strategy):
    system = (
        "You translate questions into one SQLite SELECT statement for this schema:\n"
        f"{load_schema()}\n"
        f"{STRATEGIES[strategy]}"
        "Return only the SQL, no prose, no markdown fences. SELECT statements only."
    )
    text = ask_gpt(client, system, question)
    # strip ```sql fences if the model adds them anyway
    text = re.sub(r"^```(?:sql)?\s*|\s*```$", "", text, flags=re.IGNORECASE).strip()
    return text


def run_sql(sql):
    if not sql.upper().startswith("SELECT"):
        raise ValueError("Only SELECT statements are allowed.")
    # read-only connection: even a sneaky write would fail
    conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    try:
        cur = conn.execute(sql)
        cols = [c[0] for c in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
    finally:
        conn.close()
    return rows


def make_answer(client, question, sql, rows):
    user = (
        f"Question: {question}\n"
        f"SQL used: {sql}\n"
        f"Result rows (JSON): {json.dumps(rows, default=str)}\n"
        "Answer the question in plain English, concisely."
    )
    return ask_gpt(client, "You answer questions about a books database using only the given rows.", user)


def log_turn(strategy, entry):
    path = os.path.join(HERE, f"responses_{strategy}.json")
    entries = []
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            entries = json.load(f)
    entries.append(entry)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)


def main():
    strategy = sys.argv[1] if len(sys.argv) > 1 else "zero_shot"
    if strategy not in STRATEGIES:
        sys.exit(f"Unknown strategy {strategy!r}. Choose from: {', '.join(STRATEGIES)}")

    with open(CONFIG_PATH, encoding="utf-8") as f:
        api_key = json.load(f)["openaiKey"]
    client = OpenAI(api_key=api_key)

    build_db()
    print(f"Books DB ready ({strategy}). Ask a question, or press Enter to quit.")

    while True:
        question = input("\n? ").strip()
        if not question:
            break
        entry = {"question": question, "strategy": strategy}
        try:
            sql = make_sql(client, question, strategy)
            entry["sql"] = sql
            rows = run_sql(sql)
            entry["rows"] = rows
            answer = make_answer(client, question, sql, rows)
        except Exception as e:  # ponytail: one catch-all keeps the REPL alive for the demo
            answer = f"Sorry, I couldn't answer that ({e})."
            entry["error"] = str(e)
        entry["answer"] = answer
        log_turn(strategy, entry)
        print(f"\n{answer}")
        if "sql" in entry:
            print(f"  [SQL: {entry['sql']}]")


if __name__ == "__main__":
    main()
