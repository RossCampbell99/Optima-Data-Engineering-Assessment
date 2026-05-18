from solution.main import (process_races_data, process_results_data,
                           transform_output, build_yearly_stats_df)
import pandas as pd


def make_races_df():
    races_df = pd.DataFrame({
        "raceId": [1001, 1002],
        "year": [2024, 2024],
        "round": [1, 3],
        "name": [
            "Interview Grand Prix",
            "Hello World Grand Prix"
        ],
        "date": [
            "2024-12-01",
            "2024-11-23"
        ],
        "time": [
            "17:00:00",
            "06:00:00"
        ]
    })
    return races_df


def makes_results_df():
    results_df = pd.DataFrame({
        "resultId": [100, 101, 102],
        "raceId": [1001, 1001, 1001],
        "driverId": [10, 20, 30],
        "position": [1, 2, 3],
        "fastestLapTime": [
            "01:29.4",
            "01:29.0",
            "01:29.3"
        ]
    })
    return results_df


def test_process_races_data():
    races_df = make_races_df()
    races_df = process_races_data(races_df)
    assert pd.to_datetime(races_df["datetime"], errors="coerce").notna().all()
    assert len(races_df) == 2


def test_process_races_data_bad_datetime():
    races_df = make_races_df()
    races_df['date'].iloc[0] = "bad_date"
    output = process_races_data(races_df)
    assert len(output) == len(races_df) - 1


def test_process_races_data_no_time_entry():
    races_df = make_races_df()
    races_df.loc[0, 'time'] = None
    output = process_races_data(races_df)
    assert len(output) == len(races_df)
    assert str(output['datetime'].iloc[0]) == '2024-12-01 00:00:00'


def test_process_results_data():
    results_df = makes_results_df()
    results_df = process_results_data(results_df)
    assert len(results_df) == 1
    assert results_df['position'].iloc[0] == 1
    assert results_df['driverId'].iloc[0] == 10


def test_transform_output():
    data_df = pd.DataFrame({
        "raceId": [1001, 1002],
        "year": [2024, 2024],
        "round": [2, 1],
        "name": [
            "Interview Grand Prix",
            "Hello World Grand Prix"
        ],
        "datetime": [
            "2024-12-01 17:00:00",
            "2024-03-01 12:00:00"
        ],
        "resultId": [100, 101],
        "driverId": [10, 20],
        "position": [1, 1],
        "fastestLapTime": ["01:29.4", "01:31.2"]
    })

    data_df = transform_output(data_df)

    assert list(data_df.columns) == [
        'Race Name',
        'Race Round',
        'Race Datetime',
        'Race Winning driverId',
        'Race Fastest Lap'
    ]

    expected = pd.DataFrame({
        'Race Name': [
            'Hello World Grand Prix',
            'Interview Grand Prix'
        ],
        'Race Round': [1, 2],
        'Race Datetime': [
            '2024-03-01T12:00:00.000',
            '2024-12-01T17:00:00.000'
        ],
        'Race Winning driverId': [20, 10],
        'Race Fastest Lap': [
            '01:31.2',
            '01:29.4'
        ]
    })

    pd.testing.assert_frame_equal(data_df.reset_index(drop=True), expected)


def test_build_yearly_stats_df():

    data_df = pd.DataFrame({
        'Race Name': [
            'Opening Grand Prix',
            'Interview Grand Prix',
            'Future Grand Prix'
        ],
        'Race Round': [1, 2, 1],
        'Race Datetime': [
            '2024-03-01T12:00:00.000',
            '2024-12-01T17:00:00.000',
            '2025-01-10T15:30:00.000'
        ],
        'Race Winning driverId': [20, 10, 30],
        'Race Fastest Lap': [
            '01:31.2',
            '01:29.4',
            '01:28.9'
        ]
    })

    result = build_yearly_stats_df(data_df)

    assert list(result.keys()) == [2024, 2025]

    expected_2024 = pd.DataFrame({
        'Race Name': [
            'Opening Grand Prix',
            'Interview Grand Prix'
        ],
        'Race Round': [1, 2],
        'Race Datetime': [
            '2024-03-01T12:00:00.000',
            '2024-12-01T17:00:00.000'
        ],
        'Race Winning driverId': [20, 10],
        'Race Fastest Lap': [
            '01:31.2',
            '01:29.4'
        ]
    })

    expected_2025 = pd.DataFrame({
        'Race Name': ['Future Grand Prix'],
        'Race Round': [1],
        'Race Datetime': ['2025-01-10T15:30:00.000'],
        'Race Winning driverId': [30],
        'Race Fastest Lap': ['01:28.9']
    })

    pd.testing.assert_frame_equal(
        result[2024].reset_index(drop=True),
        expected_2024
    )

    pd.testing.assert_frame_equal(
        result[2025].reset_index(drop=True),
        expected_2025
    )

# test ascii i.e. sao paolo etc is ok e2e
