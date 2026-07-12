from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "source"
START_DATE = "2025-01-01"
END_DATE = "2026-07-12"

LOCATIONS = {
    "dekalb.csv": (41.933216, -88.82266, "America/Chicago"),
    "tallahassee.csv": (30.474516, -84.28909, "America/New_York"),
    "nashville.csv": (36.168716, -86.84418, "America/Chicago"),
    "guangzhou.csv": (23.163443, 113.27749, "Asia/Shanghai"),
    "hong_kong.csv": (22.3193, 114.1694, "Asia/Hong_Kong"),
}

BASE_URL = "https://archive-api.open-meteo.com/v1/archive"


def build_url(latitude: float, longitude: float, timezone: str) -> str:
    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": START_DATE,
        "end_date": END_DATE,
        "daily": (
            "temperature_2m_mean,temperature_2m_max,temperature_2m_min"
        ),
        "temperature_unit": "celsius",
        "timezone": timezone,
        "format": "csv",
    }
    return f"{BASE_URL}?{urlencode(params)}"


def main() -> None:
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)

    for filename, (latitude, longitude, timezone) in LOCATIONS.items():
        url = build_url(latitude, longitude, timezone)
        destination = SOURCE_DIR / filename
        print(f"Downloading {filename}")
        with urlopen(url, timeout=120) as response:
            destination.write_bytes(response.read())

    print(f"Saved source data to {SOURCE_DIR}")


if __name__ == "__main__":
    main()
