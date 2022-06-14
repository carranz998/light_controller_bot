from typing import Iterator

import numpy as np
import pandas as pd


class RandomLightEvents:
    def __init__(self, s_sunrise_dates: pd.Series, s_sunset_dates: pd.Series) -> None:
        s_sunrise_dates = s_sunrise_dates \
            .drop(0) \
            .sort_values() \
            .reset_index(drop=True)

        s_sunset_dates = s_sunset_dates \
            .drop(len(s_sunset_dates)-1) \
            .sort_values() \
            .reset_index(drop=True)

        self.df_solar_events = pd.concat(
            axis='columns', 
            keys=['night_begin_timestamp', 'night_end_timestamp'],
            objs=[s_sunset_dates, s_sunrise_dates])

        self._df_events = self._build_events()

    
    @property
    def events_table(self):
        return self._df_events


    def _build_events(self) -> pd.DataFrame:
        s_events = pd.Series(self._events_per_time_range(), name='event_timestamp')
        s_events_type = pd.Series(['on', 'off'] * (len(s_events.index) // 2), name='event_type')

        df_events = pd \
            .concat([s_events, s_events_type], 'columns') \
            .set_index('event_timestamp')

        return df_events


    def _events_per_time_range(self) -> Iterator[np.ndarray]:
        for _, night_begin_timestamp, night_end_timestamp in self.df_solar_events.itertuples():
            night_events_timestamps = self._night_events_timestamps(night_begin_timestamp, night_end_timestamp)

            yield from night_events_timestamps


    def _night_events_timestamps(self, night_begin_timestamp, night_end_timestamp) -> np.ndarray:
        accumulative_distribution = np.delete(self._random_even_splittings(), [-1, -2])

        night_duration = (night_end_timestamp - night_begin_timestamp)
        night_events_timestamps = (accumulative_distribution * night_duration) + night_begin_timestamp

        return night_events_timestamps


    def _random_even_splittings(self) -> np.ndarray:
        n_samples = np.random.choice(np.arange(4, 12, 2))
        random_distribution = np.random.dirichlet(np.ones(n_samples), size=1)
        accumulative_distribution = np.cumsum(random_distribution)

        return accumulative_distribution
