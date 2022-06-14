import datetime
import os
import pathlib
from typing import Iterator, Tuple

import pandas as pd
import requests


class SolarEventsGathering:
    def __init__(self, year: int, province: str) -> None:
        self.year = year
        self.path_output_file = f'resources\\solar_events_{province}_{year}.txt'

        url = f'https://cdn.mitma.gob.es/portal-web-drupal/salidapuestasol/{year}/{province}-{year}.txt'

        if not os.path.exists(self.path_output_file):
            self.__download_file(url, pathlib.Path(self.path_output_file))

        self._s_sunrise_dates, self._s_sunset_dates = self.__solar_events()


    @property
    def s_sunrise_dates(self):
        return self._s_sunrise_dates


    @property
    def s_sunset_dates(self):
        return self._s_sunset_dates


    def __solar_events(self) -> Tuple[pd.Series, pd.Series]:
        sunrise_dates = []
        sunset_dates = []

        for sunrise_date, sunset_date in self.__parse_solar_events():
            sunrise_dates.append(sunrise_date)
            sunset_dates.append(sunset_date)

        s_sunrise_dates = pd.Series(sunrise_dates, name='sunrise_dates')
        s_sunset_dates = pd.Series(sunset_dates, name='sunset_dates')

        return s_sunrise_dates, s_sunset_dates


    def __parse_solar_events(self) -> Iterator[Tuple[datetime.datetime, datetime.datetime]]:
        with open(self.path_output_file) as f:
            valid_lines = f.readlines()[7:38]

        for line in valid_lines:
            yield from self.__parse_line(line)


    def __parse_line(self, line: str) -> Iterator[Tuple[datetime.datetime, datetime.datetime]]:
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


    def __download_file(self, input_url: str, output_path: pathlib.Path) -> None:
        with requests.get(input_url, stream=True) as response, open(output_path, 'wb+') as f:
            for chunk in response.iter_content(chunk_size=16*1024):
                f.write(chunk)
