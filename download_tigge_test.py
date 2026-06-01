import cdsapi
import pdb

dataset = "tigge-forecasts"
request = {
    "origin": "ecmwf",
    "year": "2025",
    "month": "01",
    "day": ["01", "02", "03"],
    "time": ["00:00", "12:00"],
    "level_type": "single_level",
    "variable": ["maximum_2_m_temperature_in_the_last_6_hours"],
    "forecast_type": "control_forecast",
    "leadtime_hour": ["0", "6", "12", "18"],
    "data_format": "grib",
    "area": [-10, 112, -44.5, 156.25],
    "grid": [0.125, 0.125]
}

client = cdsapi.Client()
client.retrieve(dataset, request, 'test_control.grib')
