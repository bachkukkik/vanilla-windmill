import json
import wmill

def main(grist_docs_id: str, grist_docs_table_id: str, dct_resp: dict) -> str:
    # Ensure the response contains columns
    if not (columns := dct_resp.get("columns")):
        raise ValueError("No column found")

    columns_no_formula = [col for col in columns if not col["fields"].get("formula")]
    columns_no_formula_with_id = [{"id": "id", "fields": {"type": "Int"}}] + (columns_no_formula)

    print("columns:", columns)
    print("columns_no_formula:", columns_no_formula)

    try:
        # Attempt to load type mapping from a variable
        dct_type_grist2pg = json.loads(wmill.get_variable("u/krichkorn/json_type_grist2pg"))
    except Exception as e:
        print(f"Failed to load type mapping, using default. Error: {e}")
        dct_type_grist2pg = {
            "Any": "TEXT",
            "Text": "TEXT",
            "Numeric": "NUMERIC",
            "Int": "INTEGER",
            "Bool": "BOOLEAN",
            "Date": "INTEGER",
            "DateTime": "INTEGER",
            "Choice": "TEXT",
            "ChoiceList": "JSONB",
            "Ref": "INTEGER",
            "RefList": "INTEGER[]",
            "Attachments": "BYTEA"
        }

    # Generate foreign table columns
    foreign_table_columns = ",\n".join(
        f'"{col["id"]}" {dct_type_grist2pg[col["fields"]["type"].partition(":")[0]]} NULL'
        for col in columns_no_formula_with_id
    )

    # Generate view selected columns with timestamp handling
    view_selected_columns = ",\n".join(
        (f'to_timestamp("{grist_docs_id}"."{grist_docs_table_id}"."{col["id"]}") AS "{col["id"]}"'
         if col["fields"]["type"].startswith("Date")
         else f'"{grist_docs_id}"."{grist_docs_table_id}"."{col["id"]}" AS "{col["id"]}"')
        for col in columns_no_formula_with_id
    )

    # Construct the final SQL query
    query_recreate_table = f"""
-- Create foreign table
CREATE FOREIGN TABLE "{grist_docs_id}"."{grist_docs_table_id}" (
  {foreign_table_columns}
)
SERVER "{grist_docs_id}"
OPTIONS (table '{grist_docs_table_id}');

-- Create view with timestamp
CREATE VIEW "{grist_docs_id}"."{grist_docs_table_id}_view" AS
SELECT
{view_selected_columns}
FROM "{grist_docs_id}"."{grist_docs_table_id}";
"""

    return query_recreate_table.strip()