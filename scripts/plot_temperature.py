from pathlib import Path

import pandas as pd
import plotly.graph_objects as go


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data" / "source"
PROCESSED_DIR = ROOT / "data" / "processed"
DOCS_DIR = ROOT / "docs"

FILES = {
    "DeKalb": SOURCE_DIR / "dekalb.csv",
    "Tallahassee": SOURCE_DIR / "tallahassee.csv",
    "Nashville": SOURCE_DIR / "nashville.csv",
    "Guangzhou": SOURCE_DIR / "guangzhou.csv",
    "Hong Kong": SOURCE_DIR / "hong_kong.csv",
}

COLORS = {
    "DeKalb": "#2563EB",
    "Tallahassee": "#F97316",
    "Nashville": "#16A34A",
    "Guangzhou": "#DC2626",
    "Hong Kong": "#7C3AED",
}

START_DATE = "2025-01-01"
END_DATE = "2026-07-12"


def read_open_meteo_csv(path: Path, city: str) -> pd.DataFrame:
    """Read an Open-Meteo CSV downloaded with its metadata header."""
    df = pd.read_csv(path, skiprows=3)
    df = df.rename(
        columns={
            "time": "date",
            "temperature_2m_mean (°C)": "temperature_mean_C",
            "temperature_2m_max (°C)": "temperature_max_C",
            "temperature_2m_min (°C)": "temperature_min_C",
        }
    )
    required = {
        "date",
        "temperature_mean_C",
        "temperature_max_C",
        "temperature_min_C",
    }
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{path.name} is missing columns: {sorted(missing)}")

    df["date"] = pd.to_datetime(df["date"], errors="raise")
    df["city"] = city
    return df


def build_dataset() -> pd.DataFrame:
    frames = [read_open_meteo_csv(path, city) for city, path in FILES.items()]
    data = pd.concat(frames, ignore_index=True)
    data = data.sort_values(["city", "date"]).reset_index(drop=True)

    expected = pd.date_range(START_DATE, END_DATE, freq="D")
    for city in FILES:
        city_dates = data.loc[data["city"] == city, "date"]
        missing_dates = expected.difference(city_dates)
        if len(missing_dates):
            raise ValueError(f"{city} has {len(missing_dates)} missing date(s).")

    return data


def build_figure(data: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    for city in FILES:
        subset = data.loc[data["city"] == city].sort_values("date")
        fig.add_trace(
            go.Scatter(
                x=subset["date"],
                y=subset["temperature_mean_C"],
                mode="lines",
                name=city,
                line={"color": COLORS[city], "width": 1.7},
                hovertemplate=(
                    f"<b>{city}</b><br>"
                    "Date: %{x|%Y-%m-%d}<br>"
                    "Temperature: %{y:.1f} °C"
                    "<extra></extra>"
                ),
            )
        )

    ranges = {
        "1m": [START_DATE, "2025-01-31"],
        "3m": [START_DATE, "2025-03-31"],
        "6m": [START_DATE, "2025-06-30"],
        "1y": [START_DATE, "2025-12-31"],
        "All": [START_DATE, END_DATE],
    }

    fig.update_layout(
        title={
            "text": (
                "Daily Temperature Trend"
                "<br><sup>January 1, 2025–July 12, 2026 · "
                "Hover for exact values; drag or scroll to zoom; "
                "double-click a legend item to isolate one city</sup>"
            ),
            "x": 0.5,
            "xanchor": "center",
        },
        template="plotly_white",
        width=1450,
        height=800,
        margin={"l": 85, "r": 45, "t": 125, "b": 95},
        hovermode="x unified",
        legend={
            "title": "City",
            "orientation": "h",
            "yanchor": "bottom",
            "y": 1.01,
            "xanchor": "center",
            "x": 0.5,
        },
        font={"family": "Arial, Helvetica, sans-serif", "size": 14},
        updatemenus=[
            {
                "type": "buttons",
                "direction": "left",
                "x": 0.0,
                "y": 1.17,
                "xanchor": "left",
                "yanchor": "top",
                "showactive": True,
                "buttons": [
                    {
                        "label": label,
                        "method": "relayout",
                        "args": [{"xaxis.range": date_range}],
                    }
                    for label, date_range in ranges.items()
                ],
            }
        ],
    )

    fig.update_xaxes(
        title_text="Date",
        range=ranges["All"],
        dtick="M1",
        tickformat="%b\n%Y",
        showgrid=True,
        gridcolor="rgba(100,116,139,0.16)",
        rangeslider={"visible": True, "thickness": 0.08},
    )
    fig.update_yaxes(
        title_text="Temperature (°C)",
        showgrid=True,
        gridcolor="rgba(100,116,139,0.16)",
        zeroline=True,
        zerolinecolor="rgba(100,116,139,0.35)",
    )
    return fig


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    DOCS_DIR.mkdir(parents=True, exist_ok=True)

    data = build_dataset()
    data.to_csv(PROCESSED_DIR / "daily_temperature_combined.csv", index=False)

    figure = build_figure(data)
    figure.write_html(
        DOCS_DIR / "daily_temperature_trend_interactive.html",
        include_plotlyjs="cdn",
        full_html=True,
        config={
            "scrollZoom": True,
            "displaylogo": False,
            "responsive": True,
            "toImageButtonOptions": {
                "format": "png",
                "filename": "daily_temperature_trend",
                "height": 800,
                "width": 1450,
                "scale": 2,
            },
        },
    )

    print("Created:")
    print("  data/processed/daily_temperature_combined.csv")
    print("  docs/daily_temperature_trend_interactive.html")


if __name__ == "__main__":
    main()
