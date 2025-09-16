"""
@file teil1_consistency.py
@brief Prüfung 1: Stimmigkeit der Kühlkettendaten (Paarbildung in/out, zeitliche Logik).
"""

from typing import List, Dict, Optional, Tuple


def check_consistency(records: List[Dict]) -> Tuple[bool, Optional[str]]:
    """
    @brief Prüft Stimmigkeit: zu jeder Station gibt es passende in/out-Einträge und die Reihenfolge ist logisch.
    @param records Zeitlich aufsteigende Liste von Ereignissen für genau EINE Transport-ID.
    @return (ok, fehlertext). ok=True, wenn stimmig; sonst False und eine klare Fehlerbeschreibung.
    @details Kriterien:
      - Für jede transportstation müssen Einträge in Paaren auftreten: entweder 'in' gefolgt von 'out'
        (wenn Zwischenlager) oder am Ende darf ein letztes 'in' ohne 'out' existieren, falls Transport noch läuft.
      - Es darf keine Zeitumkehr geben (nächster Eintrag < vorheriger Eintrag).
      - Kein 'in' darf zeitlich VOR dem 'out' derselben Station liegen.
      - Doppeltes 'out' oder doppeltes 'in' direkt hintereinander auf gleicher Station ist inkonsistent.
    """
    if not records:
        # Kein Eintrag ist laut Aufgabenliste auch ein möglicher Fall.
        return False, "Keine Ereignisse für diese Transport-ID gefunden."

    # 1) Zeitliche Monotonie prüfen
    for i in range(1, len(records)):
        if records[i]["datetime"] < records[i - 1]["datetime"]:
            return False, f"Zeitliche Unstimmigkeit: Ereignis {i} liegt vor Ereignis {i-1}."

    # 2) Stationen-Paarlogik prüfen
    # Wir gehen linear durch, tracken pro Station offenen Zustand.
    open_state = {}  # station -> 'in' datetime
    for idx, e in enumerate(records):
        station = e["transportstation"]
        direction = e["direction"]
        ts = e["datetime"]

        if direction not in ("in", "out"):
            return False, f"Unbekannte Richtung '{direction}' bei Station {station}."

        if direction == "in":
            if station in open_state:
                return False, f"Doppeltes 'in' ohne 'out' bei Station {station} (Pos {idx})."
            open_state[station] = ts
        else:  # out
            if station not in open_state:
                return False, f"'out' ohne vorheriges 'in' bei Station {station} (Pos {idx})."
            # Logisch: out-Zeit muss >= in-Zeit sein
            if ts < open_state[station]:
                return False, f"'out' ({ts}) liegt vor 'in' ({open_state[station]}) bei Station {station}."
            # Station abgeschlossen
            del open_state[station]

    # Am Ende: offene Stationen sind ok, WENN das der letzte Schritt ist (Transport nicht abgeschlossen).
    # Laut Aufgabenstellung ist z. B. "Auscheck-Zeitpunkt fehlt am Ende" KEIN Fehler, wenn nicht abgeschlossen.
    # Darum hier KEIN Fehler, nur Hinweis wäre möglich – aber wir bleiben beim OK.
    return True, None
