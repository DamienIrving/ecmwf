"""Command line program for downloading TIGGE data"""

import argparse
import calendar

import numpy as np
import cdsapi
#from ecmwf.datastores import Client


valid_models = ["ecmwf",]
valid_forecast_types = ["perturbed_forecast", "control_forecast"]
variables = {
    'tp': 'total_precipitation',
    'mx2t6': "maximum_2_m_temperature_in_the_last_6_hours",    
}
grids = {
    'ecmwf': [0.125, 0.125]
}
year_bounds = {
    'ecmwf': [2006, 2026],
}
area_bounds = {
   "AUS": [-10, 112, -44.5, 156.25]
}


def main(args):
    """Retrieve TIGGE data."""

    year_str = str(args.year)
    start_year, end_year = year_bounds[args.model]
    valid_years = [f'{year:.0f}' for year in np.arange(2006, 2026.1)]
    assert year_str in valid_years, f'{year_str} is not a valid year'
    
    month_str = f"{args.month:02d}"
    valid_months = [f'{int(month):02d}' for month in np.arange(1, 12.1)]
    assert month_str in valid_months, f'{month_str} is not a valid month'

    day_str = f"{args.day:02d}"
    days_in_month = calendar.monthrange(args.year, args.month)[-1]
    valid_days = [f'{int(day):02d}' for day in np.arange(1, days_in_month + 0.1)]
    assert day_str in valid_days, f'{day_str} is not a valid day'

    grid = grids[args.model]
    lead_times = [str(hour) for hour in np.arange(0, 385)]

    var_name = variables[args.var]

    dataset = "tigge-forecasts"
    request = {
        "origin": "ecmwf",
        "year": year_str,
        "month": month_str,
        "day": day_str,
        "time": ["00:00", "06:00", "12:00", "18:00"],
        "level_type": "single_level",
        "variable": [var_name],
        "forecast_type": args.forecast,
        "leadtime_hour": lead_times,
        "data_format": "grib",
        "grid": grid,
    }
    if args.area:
        request['area'] = area_bounds[args.area]
        alabel = args.area
    else:
        alabel = 'globe'
    
    flabel = args.forecast.replace('_', '-')
    outpath = f'{args.var}_{args.model}_{flabel}_{year_str}-{month_str}-{day_str}_{alabel}.grib'
    if args.d:
        print(request)
        print(outpath)
    else:
        client = cdsapi.Client()
        #client = Client()
        client.retrieve(dataset, request, outpath)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("model", choices=valid_models, type=str, help="forecast model")
    parser.add_argument("forecast", choices=valid_forecast_types, type=str, help="forecast type")
    parser.add_argument("var", choices=list(variables.keys()), type=str, help="variable")
    parser.add_argument("year", type=int, help="year")
    parser.add_argument("month", type=int, help="month")
    parser.add_argument("day", type=int, help="day")
    parser.add_argument("--area", choices=list(area_bounds.keys()), type=str, help="geographic area")
    parser.add_argument("-d", action='store_true', default=False, help="dry run (print request to screen)")
    args = parser.parse_args()
    main(args)