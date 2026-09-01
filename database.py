import json
import os
import sqlite3

conn = sqlite3.connect(
    "devops_agent.db",
    check_same_thread=False
)

cursor = conn.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("""

CREATE TABLE IF NOT EXISTS incidents(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    timestamp TEXT,

    category TEXT,

    root_cause TEXT,

    errors TEXT,

    suggestions TEXT,

    github_url TEXT,

    log_path TEXT

)

""")


def ensure_incident_column(name, definition):

    cursor.execute("PRAGMA table_info(incidents)")

    columns = [

        row[1]

        for row in cursor.fetchall()

    ]

    if name in columns:

        return False

    cursor.execute(

        f"ALTER TABLE incidents ADD COLUMN {name} {definition}"

    )

    return True


schema_changed = False
schema_changed = ensure_incident_column("status", "TEXT NOT NULL DEFAULT 'Open'") or schema_changed
schema_changed = ensure_incident_column("repository", "TEXT DEFAULT ''") or schema_changed
workflow_added = ensure_incident_column("workflow", "TEXT DEFAULT ''")
schema_changed = workflow_added or schema_changed

if workflow_added:

    cursor.execute("""

    UPDATE incidents
    SET workflow = log_path
    WHERE
        (workflow IS NULL OR workflow = '')
        AND log_path IS NOT NULL
        AND log_path != ''

    """)

cursor.execute("""

CREATE TABLE IF NOT EXISTS error_categories(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT NOT NULL UNIQUE

)

""")

cursor.execute("""

CREATE TABLE IF NOT EXISTS error_rules(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    keyword TEXT NOT NULL UNIQUE,

    category_id INTEGER NOT NULL,

    root_cause TEXT NOT NULL,

    FOREIGN KEY(category_id)
        REFERENCES error_categories(id)
        ON DELETE RESTRICT

)

""")

cursor.execute("""

CREATE TABLE IF NOT EXISTS error_suggestions(

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    rule_id INTEGER NOT NULL,

    suggestion TEXT NOT NULL,

    position INTEGER NOT NULL DEFAULT 0,

    FOREIGN KEY(rule_id)
        REFERENCES error_rules(id)
        ON DELETE CASCADE,

    UNIQUE(rule_id, position)

)

""")

conn.commit()


def add_error_rule(

    keyword,

    category,

    root_cause,

    suggestions

):

    cursor.execute(

        """

        INSERT OR IGNORE INTO error_categories(name)
        VALUES(?)

        """,

        (category,)

    )

    cursor.execute(

        """

        SELECT id
        FROM error_categories
        WHERE name = ?

        """,

        (category,)

    )

    category_id = cursor.fetchone()[0]

    cursor.execute(

        """

        INSERT INTO error_rules(
            keyword,
            category_id,
            root_cause
        )
        VALUES(?,?,?)
        ON CONFLICT(keyword) DO UPDATE SET
            category_id = excluded.category_id,
            root_cause = excluded.root_cause

        """,

        (

            keyword,

            category_id,

            root_cause

        )

    )

    cursor.execute(

        """

        SELECT id
        FROM error_rules
        WHERE keyword = ?

        """,

        (keyword,)

    )

    rule_id = cursor.fetchone()[0]

    cursor.execute(

        """

        DELETE FROM error_suggestions
        WHERE rule_id = ?

        """,

        (rule_id,)

    )

    cursor.executemany(

        """

        INSERT INTO error_suggestions(
            rule_id,
            suggestion,
            position
        )
        VALUES(?,?,?)

        """,

        [

            (

                rule_id,

                suggestion,

                position

            )

            for position, suggestion in enumerate(suggestions, start=1)

        ]

    )

    conn.commit()


def seed_error_rules(source_path="knowledge/errors.json"):

    cursor.execute("SELECT COUNT(*) FROM error_rules")

    if cursor.fetchone()[0] > 0:

        return

    if not os.path.exists(source_path):

        return

    with open(source_path, "r", encoding="utf-8") as f:

        rules = json.load(f)

    for rule in rules:

        add_error_rule(
            rule["keyword"],
            rule["category"],
            rule["root_cause"],
            rule["suggestions"]
        )


seed_error_rules()


def find_known_error(error_log):

    cursor.execute(

        """

        SELECT
            r.id,
            r.keyword,
            c.name,
            r.root_cause
        FROM error_rules r
        JOIN error_categories c
            ON c.id = r.category_id
        ORDER BY length(r.keyword) DESC

        """

    )

    for rule_id, keyword, category, root_cause in cursor.fetchall():

        if keyword.lower() in error_log.lower():

            cursor.execute(

                """

                SELECT suggestion
                FROM error_suggestions
                WHERE rule_id = ?
                ORDER BY position

                """,

                (rule_id,)

            )

            suggestions = [

                row[0]

                for row in cursor.fetchall()

            ]

            return {

                "keyword": keyword,

                "category": category,

                "root_cause": root_cause,

                "suggestions": suggestions

            }

    return None


def save_incident(

    timestamp,

    category,

    root_cause,

    errors,

    suggestions,

    github_url="",

    log_path="",

    repository="",

    workflow="",

    status="Open"

):

    if github_url.startswith(("http://", "https://")) and incident_exists(github_url):

        return

    cursor.execute(

        """

        INSERT INTO incidents(

        timestamp,

        category,

        root_cause,

        errors,

        suggestions,

        github_url,

        log_path,

        repository,

        workflow,

        status

        )

        VALUES(

        ?,?,?,?,?,?,?,?,?,?

        )

        """,

        (

            timestamp,

            category,

            root_cause,

            errors,

            suggestions,

            github_url,

            log_path,

            repository,

            workflow,

            status

        )

    )

    conn.commit()


def update_incident_status(repository, workflow, status):

    cursor.execute(

        """

        UPDATE incidents
        SET status = ?
        WHERE id = (
            SELECT id
            FROM incidents
            WHERE repository = ?
                AND workflow = ?
            ORDER BY id DESC
            LIMIT 1
        )

        """,

        (

            status,

            repository,

            workflow

        )

    )

    conn.commit()

    return cursor.rowcount


def incident_exists(github_url):

    cursor.execute(

        """

        SELECT 1
        FROM incidents
        WHERE github_url = ?
        LIMIT 1

        """,

        (github_url,)

    )

    return cursor.fetchone() is not None


def get_all():

    cursor.execute(

        """

        SELECT *

        FROM incidents

        ORDER BY id DESC

        """

    )

    return cursor.fetchall()


def find_similar(

    error_text

):

    cursor.execute(

        """

        SELECT

        timestamp,

        category,

        root_cause,

        suggestions,

        github_url,

        log_path

        FROM incidents

        WHERE errors LIKE ?

        ORDER BY id DESC

        LIMIT 1

        """,

        (

            "%"+error_text[:25]+"%",

        )

    )

    return cursor.fetchone()
