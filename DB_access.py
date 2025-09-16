"""
@file db_access.py
@brief Einfache DB-Zugriffsschicht für CoolChain (pyodbc). Nutzt env-Variablen, damit keine Klartext-PW im Code liegen.
"""

import os
from typing import List, Dict

try:
    import pyodbc  # type: ignore
except ImportError:
    pyodbc = None  # damit der Code auch ohne Treiber importierbar bleibt


def _conn_str() -> str:
    """
    @brief Baut den Verbindungsstring aus Umgebungsvariablen.
    @return ODBC-Verbindungsstring.
    @details Erwartete Variablen:
     - CC_SQL_SERVER
     - CC_SQL_DB
     - CC_SQL_USER
     - CC_SQL_PWD
     Falls nicht gesetzt, werden die in der Aufgabenstellung genannten Defaults verwendet (nur Schulumgebung!).
    """
    server = os.getenv("CC_SQL_SERVER", "sc-db-server.database.windows.net")
    database = os.getenv("CC_SQL_DB", "supplychain")
    user = os.getenv("CC_SQL_USER", "rse")
    pwd = os.getenv("CC_SQL_PWD", "Pa$$w0rd")
    driver = os.getenv("CC_SQL_DRIVER", "ODBC Driver 17 for SQL Server")
    return f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={user};PWD={pwd}"


def fetch_records(company: str, transport_id: str) -> List[Dict]:
    """
    @brief Lädt alle Coolchain-Ereignisse (in/out je Station) für eine Transport-ID.
    @param company Firmenname/Index, z. B. "Food Solution Hildesheim".
    @param transport_id Transport-ID als String.
    @return Liste von Dicts mit Schlüsseln: company, transportid, transportstation, category, direction, datetime.
    @throws RuntimeError wenn pyodbc nicht installiert oder DB nicht erreichbar.
    """
    if pyodbc is None:
        raise RuntimeError("pyodbc nicht installiert. Bitte 'pip install pyodbc' und passenden ODBC-Treiber setzen.")

    sql = """
        SELECT company, transportid, transportstation, category, direction, datetime
        FROM dbo.coolchain
        WHERE company = ? AND transportid = ?
        ORDER BY datetime ASC
    """

    with pyodbc.connect(_conn_str()) as conn:
        cur = conn.cursor()
        rows = cur.execute(sql, (company, transport_id)).fetchall()

    out: List[Dict] = []
    for r in rows:
        out.append({
            "company": r[0],
            "transportid": r[1],
            "transportstation": r[2],
            "category": r[3],
            "direction": r[4],       # 'in' oder 'out'
            "datetime": r[5],        # datetime aus SQL
        })
    return out
