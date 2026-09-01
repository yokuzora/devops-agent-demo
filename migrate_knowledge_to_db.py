import json

from database import add_error_rule


def migrate(
    source_path="knowledge/errors.json"
):

    with open(source_path, "r", encoding="utf-8") as f:
        rules = json.load(f)

    for rule in rules:

        add_error_rule(
            rule["keyword"],
            rule["category"],
            rule["root_cause"],
            rule["suggestions"]
        )

    return len(rules)


if __name__ == "__main__":

    count = migrate()
    print(f"Migrated {count} knowledge rules into SQLite.")
