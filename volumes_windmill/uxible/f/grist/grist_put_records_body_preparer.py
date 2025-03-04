from typing import List

def main(
    records: list,
    cols_keys: List[str],
):
    lst_body = []
    for r in records:
        lst_body.append(
            {
                "require": {
                    k: v for k, v in r.items() if k in cols_keys
                },
                "fields": {
                    k: v for k, v in r.items() if k not in cols_keys
                }
            }
        )

    body = {"records": lst_body}
    return body
    