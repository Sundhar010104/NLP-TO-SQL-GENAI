import re

BLOCKED_KEYWORDS = [
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE",
    "ATTACH",
    "DETACH",
    "PRAGMA",
    "VACUUM"
]

def validate_sql(sql: str):
    if not sql:
        return False, "Empty SQL query."

    sql = sql.strip()

    # Block multiple statements
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    if len(statements) > 1:
        return False, "Multiple SQL statements are not allowed."

    sql = statements[0]

    # Only SELECT or WITH (CTEs)
    if not (
        sql.upper().startswith("SELECT")
        or sql.upper().startswith("WITH")
    ):
        return False, "Only SELECT queries are allowed."

    upper_sql = sql.upper()

    for keyword in BLOCKED_KEYWORDS:
        if re.search(rf"\b{keyword}\b", upper_sql):
            return False, f"Blocked keyword: {keyword}"

    return True, "Valid SQL"