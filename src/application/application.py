from data_gathering.solar_events_gathering import SolarEventsGathering


class Application:
    def __init__(self) -> None:
        table = SolarEventsGathering(2022, 'Barcelona')

        s_sunrise_dates = table.s_sunrise_dates
        s_sunset_dates = table.s_sunset_dates

        print(s_sunrise_dates)
        print(s_sunset_dates)
