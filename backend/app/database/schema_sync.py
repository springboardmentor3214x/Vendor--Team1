from sqlalchemy import inspect, text
from sqlalchemy.schema import CreateColumn
from app.database.base import Base

def sync_schema(engine) -> list:
    inspector = inspect(engine)
    existing_tables = set(inspector.get_table_names())
    added = []

    for table in Base.metadata.sorted_tables:
        if table.name not in existing_tables:
            continue

        db_columns = {col["name"] for col in inspector.get_columns(table.name)}

        for column in table.columns:
            if column.name in db_columns:
                continue

            ddl = str(CreateColumn(column).compile(engine)).strip()
            ddl = ddl.replace(" NOT NULL", "")

            with engine.begin() as connection:
                connection.execute(
                    text(f'ALTER TABLE "{table.name}" ADD COLUMN IF NOT EXISTS {ddl}')
                )
            added.append(f"{table.name}.{column.name}")

    return added


def _pending_schema_sync_rows(items):
    rows = []
    for item in items:
        rows.append({
            "id": getattr(item, "id", None),
            "label": str(getattr(item, "name", "")),
            "state": getattr(item, "status", "Pending"),
        })
    return rows


def _pending_schema_sync_totals(items):
    totals = {"count": len(items), "active": 0}
    for item in items:
        if getattr(item, "status", "") == "Active":
            totals["active"] += 1
    return totals
