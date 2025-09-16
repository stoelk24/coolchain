"""
@file teil2_transfer_gaps.py
@brief Prüfung 2: Übergabezeiten zwischen Stationen (Zeit ohne Kühlung <= 10 Minuten).
"""

from typing import List, Dict, Optional, Tuple
from datetime import timedelta


def check_transfer_gaps(records: List[Dict], max_gap_minutes: int = 10) -> Tuple[bool, Optional[str]]:
    """
    @brief Prüft, ob zwischen 'out' einer Station und dem folgenden 'in' der nächsten Station die Lücke <= 10 min liegt.
    @param records Zeitlich sortierte Ereignisliste für genau EINE Transport-ID.
    @param max_gap_minutes Obergrenze in Minuten (Default 10).
    @return (ok, fehlertext). Bei Verstoß: False und Beschreibung inkl. betroffener Stationen und Gap.
    @details Vorgehen:
      - Finde jede Sequenz … [Station A 'out'] → [Station B 'in'] …
      - Berechne Differenz in Minuten. Wenn > max_gap_minutes → Fehler.
      - Falls Transport nicht abgeschlossen (letztes Ereignis 'in' ohne späteres 'out'), kein spezieller Fehler hier.
    """
    if not records:
        return False, "Keine Ereignisse vorhanden."

    # Wir suchen Paare aus out (Station A) gefolgt von in (Station B) im NÄCHSTEN Ereignis,
    # unabhängig davon, ob B == A ist (Sonderfälle werden durch Konsistenzprüfung abgefangen).
    max_gap = timedelta(minutes=max_gap_minutes)

    for i in range(len(records) - 1):
        a = records[i]
        b = records[i + 1]
        if a["direction"] == "out" and b["direction"] == "in":
            gap = b["datetime"] - a["datetime"]
            if gap > max_gap:
                return (
                    False,
                    f"Übergabe > {max_gap_minutes} min: {a['transportstation']} (out @ {a['datetime']}) → "
                    f"{b['transportstation']} (in @ {b['datetime']}) = {int(gap.total_seconds() // 60)} min."
                )

    return True, None
