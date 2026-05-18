import pandas as pd
import json
import logging

logger = logging.getLogger('data-engineering-solution')

RACES_PATH = "source-data/races.csv"
RESULTS_PATH = "source-data/results.csv"


def main():
    raw_races_df = pd.read_csv(RACES_PATH)
    races_df = process_races_data(raw_races_df)

    raw_results_df = pd.read_csv(RESULTS_PATH)
    results_df = process_results_data(raw_results_df)

    data_df = pd.merge(left=races_df, right=results_df, on='raceId')
    data_df = transform_output(data_df)
    stats_by_year = build_yearly_stats_df(data_df)
    export_stats(stats_by_year)


def process_races_data(races_df):
    races_df['time'] = races_df['time'].fillna("00:00:00")
    races_df['datetime'] = pd.to_datetime(races_df['date'].astype(str) + 
                                        ' ' + 
                                        races_df['time'].astype(str),
                                        errors="coerce")
    
    failed = races_df[races_df['datetime'].isna()]
    races_df = races_df.dropna(subset=['datetime'])
    if not failed.empty:
        logger.warning(f"{len(failed)} rows failed datetime parsing")
        logger.warning(
            "Failed rows (date, time):\n%s",
            failed.to_string(index=False)
        )
    return races_df


def process_results_data(results_df):
    results_df = results_df.dropna(subset=["position"])
    winners_df = results_df.loc[results_df["position"].astype(int) == 1]
    logger.info(f'Total races in results.csv are {len(winners_df)}')
    return winners_df


def transform_output(data_df):
    data_df['roud'] = data_df['round'].astype(int)
    data_df['driverId'] = data_df['driverId'].astype(int)
    # only want first 3 digits of milliseconds as requested by client
    data_df['datetime'] = pd.to_datetime(data_df['datetime'])
    data_df['datetime'] = data_df['datetime'].dt.strftime('%Y-%m-%dT%H:%M:%S.%f').str[:-3]
    data_df = data_df.sort_values('datetime')
    data_df['fastestLapTime'].fillna('No Data', inplace=True)

    data_df = data_df.drop_duplicates().dropna()

    data_df = data_df[['name', 'round', 'datetime', 'driverId', 'fastestLapTime']]
    data_df = data_df.rename(columns={'name': 'Race Name',
                                      'round': 'Race Round',
                                      'datetime': 'Race Datetime',
                                      'driverId': 'Race Winning driverId',
                                      'fastestLapTime': 'Race Fastest Lap'})

    return data_df


def build_yearly_stats_df(data_df):
    return {
        year: df_year
        for year, df_year in data_df.groupby(pd.to_datetime(data_df['Race Datetime']).dt.year)
    }


def export_stats(grouped_data):
    for year, df_year in grouped_data.items():
        with open(f"results/stats_{year}.json", "w", encoding="utf-8") as f:
            json.dump(
                df_year.to_dict(orient="records"),
                f,
                indent=4,
                ensure_ascii=False
            )


if __name__ == "__main__":
    main()
