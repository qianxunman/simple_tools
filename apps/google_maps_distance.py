"""Utilities for summing daily driving distance with optional waypoints.

The script reads trip data (CSV/Excel) with columns:
- name: person identifier
- date: trip date
- origin: starting address
- destination: ending address
- waypoints (optional): intermediate stops separated by a custom delimiter (default: "|")

It queries the Google Maps Directions API so that waypoints are respected.
Set the API key via the GOOGLE_MAPS_API_KEY environment variable or the --api-key flag.
"""

from __future__ import annotations

import argparse
import os
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import pandas as pd
import requests

DIRECTIONS_URL = "https://maps.googleapis.com/maps/api/directions/json"
DEFAULT_WAYPOINT_SEPARATOR = "|"


class DirectionsApiError(RuntimeError):
    """Raised when the Directions API returns a non-OK status."""


def _normalize_waypoints(value: Optional[object], separator: str) -> List[str]:
    if value is None:
        return []
    if isinstance(value, float) and pd.isna(value):
        return []
    if isinstance(value, (list, tuple, set)):
        raw_points: Iterable[str] = value
    else:
        raw_points = str(value).split(separator)
    return [point.strip() for point in raw_points if str(point).strip()]


def _cache_key(origin: str, destination: str, waypoints: Sequence[str]) -> Tuple[str, str, Tuple[str, ...]]:
    return (origin.strip(), destination.strip(), tuple(waypoints))


def fetch_route_distance_km(
    origin: str,
    destination: str,
    waypoints: Optional[Sequence[str]] = None,
    *,
    api_key: Optional[str] = None,
    session: Optional[requests.Session] = None,
) -> float:
    """Fetch the driving distance in kilometers for a route with optional waypoints."""

    key = api_key or os.getenv("GOOGLE_MAPS_API_KEY")
    if not key:
        raise ValueError("Google Maps API key is required (pass --api-key or set GOOGLE_MAPS_API_KEY).")

    params = {
        "origin": origin,
        "destination": destination,
        "mode": "driving",
        "key": key,
    }
    if waypoints:
        params["waypoints"] = "|".join(waypoints)

    http = session or requests.Session()
    response = http.get(DIRECTIONS_URL, params=params, timeout=10)
    response.raise_for_status()
    payload = response.json()

    if payload.get("status") != "OK":
        raise DirectionsApiError(
            f"Directions API status={payload.get('status')} message={payload.get('error_message', '')}"
        )

    legs = payload.get("routes", [{}])[0].get("legs", [])
    if not legs:
        raise DirectionsApiError("Directions API returned no legs for the requested route.")

    distance_meters = sum(leg["distance"]["value"] for leg in legs)
    return distance_meters / 1000.0


def calculate_daily_distances(
    trips: pd.DataFrame,
    *,
    waypoint_separator: str = DEFAULT_WAYPOINT_SEPARATOR,
    api_key: Optional[str] = None,
) -> pd.DataFrame:
    """Compute total kilometers per person per day, honoring intermediate waypoints."""

    required = {"name", "date", "origin", "destination"}
    missing = required - set(trips.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    trips = trips.copy()
    trips["date"] = pd.to_datetime(trips["date"]).dt.date

    cache: Dict[Tuple[str, str, Tuple[str, ...]], float] = {}
    session = requests.Session()

    def compute_row_km(row: pd.Series) -> float:
        waypoints = _normalize_waypoints(row.get("waypoints"), waypoint_separator)
        key = _cache_key(row.origin, row.destination, waypoints)
        if key in cache:
            return cache[key]
        km = fetch_route_distance_km(
            row.origin,
            row.destination,
            waypoints=waypoints,
            api_key=api_key,
            session=session,
        )
        cache[key] = km
        return km

    trips["km"] = trips.apply(compute_row_km, axis=1)
    return trips.groupby(["name", "date"])['km'].sum().reset_index()


def _read_table(path: str) -> pd.DataFrame:
    if path.lower().endswith((".xls", ".xlsx")):
        return pd.read_excel(path)
    return pd.read_csv(path)


def _write_table(df: pd.DataFrame, path: str) -> None:
    if path.lower().endswith((".xls", ".xlsx")):
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Sum daily driving distance with Google Maps waypoints support.")
    parser.add_argument("--input", required=True, help="Input CSV/Excel file with trips.")
    parser.add_argument("--output", required=True, help="Where to write the aggregated CSV/Excel output.")
    parser.add_argument("--api-key", dest="api_key", help="Google Maps API key (otherwise use GOOGLE_MAPS_API_KEY env var).")
    parser.add_argument(
        "--waypoint-separator",
        default=DEFAULT_WAYPOINT_SEPARATOR,
        help=f"Delimiter for the waypoints column (default: '{DEFAULT_WAYPOINT_SEPARATOR}').",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    trips = _read_table(args.input)
    result = calculate_daily_distances(
        trips,
        waypoint_separator=args.waypoint_separator,
        api_key=args.api_key,
    )
    _write_table(result, args.output)


if __name__ == "__main__":
    main()
