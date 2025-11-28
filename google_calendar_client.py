# google_calendar_client.py

from __future__ import annotations

from datetime import datetime
from typing import List, Dict, Optional

import os
import pickle

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from config import (
    GOOGLE_CALENDAR_SCOPES,
    GOOGLE_CALENDAR_CREDENTIALS_FILE,
    GOOGLE_CALENDAR_TOKEN_FILE,
    GOOGLE_CALENDAR_CALENDAR_ID,
    TIMEZONE,
)


class GoogleCalendarClient:
    """
    Cliente para interactuar con Google Calendar usando OAuth 2.0.

    Encapsula:
    - Autenticación
    - Listado de eventos
    - Creación de eventos
    - Eliminación de eventos
    """

    def __init__(self) -> None:
        self.service = self._get_service()

    def _get_service(self):
        creds = None

        # token.pickle / token.json (token ya generado previamente)
        if os.path.exists(GOOGLE_CALENDAR_TOKEN_FILE):
            with open(GOOGLE_CALENDAR_TOKEN_FILE, "rb") as token:
                creds = pickle.load(token)

        # Si no hay credenciales válidas, iniciar flujo OAuth
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_CALENDAR_CREDENTIALS_FILE,
                    GOOGLE_CALENDAR_SCOPES,
                )
                creds = flow.run_local_server(port=0)

            # Guardar token para futuras ejecuciones
            with open(GOOGLE_CALENDAR_TOKEN_FILE, "wb") as token:
                pickle.dump(creds, token)

        service = build("calendar", "v3", credentials=creds)
        return service

    def _parse_to_iso(self, fecha_hora: str) -> str:
        """
        Convierte 'YYYY-MM-DD HH:MM' a ISO 8601 con timezone.
        Ejemplo: '2025-11-28 10:00' -> '2025-11-28T10:00:00+01:00'
        """
        # Ajusta el formato si quieres aceptar otros
        dt = datetime.strptime(fecha_hora, "%Y-%m-%d %H:%M")
        # NO ponemos offset manual, dejamos que Google use la TZ
        return dt.isoformat()

    def list_events(
        self,
        fecha_inicio: str,
        fecha_fin: str,
        max_resultados: int = 10,
    ) -> List[Dict]:
        """
        Lista eventos entre fecha_inicio y fecha_fin (formato 'YYYY-MM-DD HH:MM').
        """
        time_min = self._parse_to_iso(fecha_inicio)
        time_max = self._parse_to_iso(fecha_fin)

        events_result = (
            self.service.events()
            .list(
                calendarId=GOOGLE_CALENDAR_CALENDAR_ID,
                timeMin=time_min,
                timeMax=time_max,
                maxResults=max_resultados,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )

        events = events_result.get("items", [])
        simplified = []

        for e in events:
            simplified.append(
                {
                    "id": e.get("id"),
                    "summary": e.get("summary"),
                    "description": e.get("description"),
                    "location": e.get("location"),
                    "start": e.get("start", {}).get("dateTime")
                    or e.get("start", {}).get("date"),
                    "end": e.get("end", {}).get("dateTime")
                    or e.get("end", {}).get("date"),
                }
            )

        return simplified

    def create_event(
        self,
        titulo: str,
        fecha_inicio: str,
        fecha_fin: str,
        descripcion: Optional[str] = None,
        ubicacion: Optional[str] = None,
    ) -> Dict:
        """
        Crea un evento en Google Calendar.
        Las fechas se reciben como 'YYYY-MM-DD HH:MM'.
        """
        start_iso = self._parse_to_iso(fecha_inicio)
        end_iso = self._parse_to_iso(fecha_fin)

        event_body = {
            "summary": titulo,
            "description": descripcion or "",
            "location": ubicacion or "",
            "start": {
                "dateTime": start_iso,
                "timeZone": TIMEZONE,
            },
            "end": {
                "dateTime": end_iso,
                "timeZone": TIMEZONE,
            },
        }

        event = (
            self.service.events()
            .insert(calendarId=GOOGLE_CALENDAR_CALENDAR_ID, body=event_body)
            .execute()
        )

        return {
            "id": event.get("id"),
            "htmlLink": event.get("htmlLink"),
            "summary": event.get("summary"),
        }

    def delete_event(self, event_id: str) -> Dict:
        """
        Elimina un evento por su ID de Google Calendar.
        """
        self.service.events().delete(
            calendarId=GOOGLE_CALENDAR_CALENDAR_ID,
            eventId=event_id,
        ).execute()

        return {"status": "deleted", "id": event_id}
