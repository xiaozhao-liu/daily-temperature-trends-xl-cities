# Daily Temperature Trends Across XL's Cities

Interactive daily temperature comparison for **DeKalb, Tallahassee, Nashville, Guangzhou, and Hong Kong**—cities where I have lived or currently live—covering **January 1, 2025 to July 12, 2026**.

## Interactive plot

After GitHub Pages is enabled, open:

**https://xiaozhao-liu.github.io/daily-temperature-trends-xl-cities/daily_temperature_trend_interactive.html**

The chart supports hover values, scroll/drag zoom, a range slider, city visibility controls, and fixed date-range buttons starting from January 1, 2025.

## Data source

Data were downloaded from the [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api).

Daily variables:

- `temperature_2m_mean`
- `temperature_2m_max`
- `temperature_2m_min`

The source files are stored in [`data/source`](data/source). These are coordinate-based Open-Meteo historical weather records, not direct campus weather-station measurements.

## Download source data

Open the [Open-Meteo Historical Weather API page](https://open-meteo.com/en/docs/historical-weather-api), then set:

1. Location coordinates
2. Start date: `2025-01-01`
3. End date: `2026-07-12`
4. Daily weather variables: mean, maximum, and minimum 2 m temperature
5. Temperature unit: Celsius
6. Output format: CSV

Example API pattern:

```text
https://archive-api.open-meteo.com/v1/archive?latitude=LAT&longitude=LON&start_date=2025-01-01&end_date=2026-07-12&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&temperature_unit=celsius&timezone=auto&format=csv
```

## Logic

1. Read each Open-Meteo CSV while skipping its three-line metadata header.
2. Standardize the temperature column names.
3. Verify that every city contains the full daily date range.
4. Combine all cities into one processed CSV.
5. Plot every daily mean-temperature value as an interactive continuous line.
6. Export the HTML chart for GitHub Pages.

## Repository structure

```text
daily-temperature-trends-xl-cities/
├── data/
│   ├── source/       # Original Open-Meteo CSV files
│   └── processed/    # Combined daily dataset
├── docs/
│   └── daily_temperature_trend_interactive.html
├── scripts/
│   └── plot_temperature.py
├── requirements.txt
└── README.md
```

## Reproduce the plot

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/plot_temperature.py
```

On Windows PowerShell, activate the environment with:

```powershell
.venv\Scripts\Activate.ps1
```

The script recreates:

- `data/processed/daily_temperature_combined.csv`
- `docs/daily_temperature_trend_interactive.html`
