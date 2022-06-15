from ast import Tuple
import datetime
import pathlib
import numpy as np

import pandas as pd


class SolarEventsGathering:
    def __init__(self, input_filepath: pathlib.Path) -> None:
        self.year = 2022
        self.path_output_file = input_filepath

        self._s_sunrise_dates, self._s_sunset_dates = self.__solar_events()

    @property
    def s_sunrise_dates(self):
        return self._s_sunrise_dates


    @property
    def s_sunset_dates(self):
        return self._s_sunset_dates


    def __solar_events(self):
        solar_events = np.array(list(self.__parse_solar_events()), dtype=np.datetime64).T

        s_sunrise_dates = pd.Series(solar_events[0], name='sunrise_dates')
        s_sunset_dates = pd.Series(solar_events[1], name='sunset_dates')

        return s_sunrise_dates, s_sunset_dates


    def __parse_solar_events(self):
        with open(self.path_output_file) as f:
            valid_lines = f.readlines()[7:38]

        for line in valid_lines:
            yield from self.__parse_line(line)


    def __parse_line(self, line: str):
        for month, i in enumerate(range(3, 123, 10), 1):
            try:
                day = int(line[0: 2])
                hour_sunrise = int(line[i])
                minute_sunrise = int(line[i+1: i+3])

                hour_sunset = int(line[i+4: i+6])
                minute_sunset = int(line[i+6: i+8])

                sunrise_date = datetime.datetime(self.year, month, day, hour_sunrise, minute_sunrise)
                sunset_date = datetime.datetime(self.year, month, day, hour_sunset, minute_sunset)

                yield sunrise_date, sunset_date
            except ValueError:
                pass
