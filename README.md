# Daily Temperature Trends Across XL's Cities

Interactive daily temperature comparison for **Guangzhou, DeKalb, Tallahassee, Nashville, and Hong Kong**—cities where I have lived or currently live—covering **January 1, 2025 to July 12, 2026**.

## Interactive plot

Open the published chart:

**https://xiaozhao-liu.github.io/daily-temperature-trends-xl-cities/plot/daily_temperature_trend_interactive.html**

The chart uses every daily temperature value as a continuous line. It supports:

- hover labels with city, date, and temperature
- drag and scroll zoom
- a date-range slider
- quick ranges beginning on January 1, 2025
- legend controls; double-click a city to isolate it

## Data source

The data were downloaded from the [Open-Meteo Historical Weather API](https://open-meteo.com/en/docs/historical-weather-api).

Daily variables:

- `temperature_2m_mean`
- `temperature_2m_max`
- `temperature_2m_min`

Temperature unit: **degrees Celsius**.

The original downloaded CSV files are stored in [`source-data/`](source-data/). The interactive HTML plot is stored in [`plot/`](plot/).

> These are coordinate-based Open-Meteo historical weather data, not direct measurements from university or campus weather stations.

## Direct CSV download links

Each link downloads daily mean, maximum, and minimum 2 m air temperature from `2025-01-01` through `2026-07-12` in CSV format.

### DeKalb

```text
https://archive-api.open-meteo.com/v1/archive?latitude=41.933216&longitude=-88.82266&start_date=2025-01-01&end_date=2026-07-12&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&temperature_unit=celsius&timezone=auto&format=csv
```

### Tallahassee

```text
https://archive-api.open-meteo.com/v1/archive?latitude=30.474516&longitude=-84.28909&start_date=2025-01-01&end_date=2026-07-12&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&temperature_unit=celsius&timezone=auto&format=csv
```

### Nashville

```text
https://archive-api.open-meteo.com/v1/archive?latitude=36.168716&longitude=-86.84418&start_date=2025-01-01&end_date=2026-07-12&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&temperature_unit=celsius&timezone=auto&format=csv
```

### Guangzhou

```text
https://archive-api.open-meteo.com/v1/archive?latitude=23.163443&longitude=113.27749&start_date=2025-01-01&end_date=2026-07-12&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&temperature_unit=celsius&timezone=auto&format=csv
```

### Hong Kong

```text
https://archive-api.open-meteo.com/v1/archive?latitude=22.319859&longitude=114.198555&start_date=2025-01-01&end_date=2026-07-12&daily=temperature_2m_mean,temperature_2m_max,temperature_2m_min&temperature_unit=celsius&timezone=auto&format=csv
```

To download a file, paste its URL into a browser. Open-Meteo will return a CSV containing a metadata header followed by one row per day.

## Plotting logic

1. Read the five Open-Meteo CSV files and skip the three-line metadata header.
2. Convert the date column to a date-time format.
3. Standardize the mean, maximum, and minimum temperature column names.
4. Combine the city datasets and verify the daily date range.
5. Plot the daily mean temperature for each city as a continuous interactive line.
6. Export the Plotly chart as `plot/daily_temperature_trend_interactive.html`.

## Repository structure

```text
daily-temperature-trends-xl-cities/
├── source-data/                           # Manually uploaded Open-Meteo CSV files
├── plot/
│   └── daily_temperature_trend_interactive.html
├── scripts/
│   ├── download_data.py
│   └── plot_temperature.py
├── .github/workflows/
│   └── build-temperature-data.yml
├── requirements.txt
└── README.md
```

## Python requirements

```text
pandas>=2.0
plotly>=5.20
```
