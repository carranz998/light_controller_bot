from data_gathering.solar_events_gathering import SolarEventsGathering
from data_processing.random_light_events import RandomLightEvents


class Application:
    def __init__(self) -> None:
        table = SolarEventsGathering(2022, 'Barcelona')

        s_sunrise_dates = table.s_sunrise_dates
        s_sunset_dates = table.s_sunset_dates

        random_light_events = RandomLightEvents(s_sunrise_dates, s_sunset_dates)
        events_table = random_light_events.events_table

        print(events_table)
