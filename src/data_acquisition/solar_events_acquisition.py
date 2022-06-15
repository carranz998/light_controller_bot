import os
import pathlib

import requests


class SolarEventsAcquisition:
    @classmethod
    def acquire_events_table(cls, year: int, spain_province: str) -> pathlib.Path:
        path_output_file = pathlib.Path(f'resources\\solar_events_{spain_province}_{year}.txt')
        url = f'https://cdn.mitma.gob.es/portal-web-drupal/salidapuestasol/{year}/{spain_province}-{year}.txt'

        if not os.path.exists(path_output_file):
            cls.__download_file(url, path_output_file)

        return path_output_file


    @classmethod
    def __download_file(cls, input_url: str, output_path: pathlib.Path) -> None:
        response = requests.get(input_url, stream=True)
        output_file = open(output_path, 'wb+')

        with response, output_file:
            for chunk in response.iter_content(chunk_size=16*1024):
                output_file.write(chunk)
