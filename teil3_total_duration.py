"""
@file teil3_total_duration.py
@brief Prüfung 3: Gesamtdauer des Transports (<= 48 Stunden).
"""

from typing import List, Dict, Optional, Tuple
from datetime import timedelta


def check_total_duration(records: List[Dict], max_hours: int = 48) -> Tuple[bool, Optional[str]]:
    """
    @brief Prüft, ob die Gesamtdauer zwischen dem ersten Ereignis und dem letzten 'out' <= 48h bleibt.
    @param records Zeitlich sortierte Ereignisliste für genau EINE Transport-ID.
    @param max_hours Obergrenze in Stunden (Default 48).
    @return (ok, fehlertext). Bei Überschreitung: False und konkrete Dauerangabe.
    @details Logik:
      - Startzeit = Timestamp des ERSTEN Ereignisses.
      - Endzeit = Timestamp des LETZTEN Ereignisses. Wenn letzter Eintrag ein 'in' ist (Transport läuft),
        verwenden wir den letzten vorhandenen Timestamp (konservativ).
      - Dauer = Endzeit - Startzeit.
    """
    if not records:
        return False, "Keine Ereignisse vorhanden."

    start = records[0]["datetime"]
    end = records[-1]["datetime"]
    duration = end - start
    if duration > timedelta(hours=max_hours):
        total_h = int(duration.total_seconds() // 3600)
        return False, f"Transportdauer > {max_hours}h: insgesamt ~{total_h}h (von {start} bis {end})."
    return True, None
