#!/usr/bin/env python3
"""
Tool for generating ADGSBOA metrics for prometheus

Written by DEIMOS Space S.L. (dibb)

module adgsboa
"""
# Import python utilities
import argparse
import datetime
from dateutil import parser
from dateutil import relativedelta
import tempfile
import shutil
import os

# Import query
from eboa.engine.query import Query

# Import logging
from eboa.logging import Log

logging = Log(name = __name__, log_name = "eboa_metrics.log")
logger = logging.logger

def execute_generator(begin, end, metrics_file_path):
    """Function to generate the metrics from the ADGSBOA
    
    :param begin: start date of the period to generate metrics
    :type begin: str
    :param end: stop date of the period to generate metrics
    :type end: str
    :param metrics_file_path: path to the output metrics file
    :type metrics_file_path: str
    """

    logger.info(f"Generating ADGSBOA metrics to path {metrics_file_path} using the following window: [{begin}, {end}]")
    
    # Temporary file is moved to the final destination once closed
    temporary_file = tempfile.NamedTemporaryFile(delete=False)
    temporary_file_path = temporary_file.name

    f= open(temporary_file_path,"w+")
    
    # Create query object
    query = Query()

    # Status of adgsboa metrics
    adgsboa_metrics_up = 1

    # Obtain relevant events
    day_start = parser.parse(end[0:10]).isoformat()
    day_stop = (parser.parse(end[0:10]) + datetime.timedelta(days=1)).isoformat()
    month_start = parser.parse(end[0:7] + "-01").isoformat()
    month_stop = (parser.parse(end[0:7] + "-01") + relativedelta.relativedelta(months=1)).isoformat()

    #####################
    # DOWNLOADED VOLUME #
    #####################
    # CUMULATIVE_DOWNLOADED_VOLUME_PER_DAY
    cumulative_downloaded_volume_per_day_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_VOLUME_PER_DAY_{day_start}_{day_stop}", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_downloaded_volume_per_day_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded volume from AUXIP per day")
    else:
        event = cumulative_downloaded_volume_per_day_events[0]
        metric_name = "auxip_cumulative_downloaded_volume_per_day"
        f.write(
f'''# HELP {metric_name} Cumulated downloaded volume from AUXIP per day.
# TYPE {metric_name} gauge
{metric_name} {event.eventDoubles[0].value}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if
    
    # CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_DAY
    cumulative_downloaded_volume_by_client_per_day_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_DAY_{day_start}_{day_stop}", "op": "=="}
    )
    if len(cumulative_downloaded_volume_by_client_per_day_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded volume by client from AUXIP per day")
    else:
        for event in cumulative_downloaded_volume_by_client_per_day_events:
            client = event.gauge.system
            metric_name = "auxip_cumulative_downloaded_volume_by_client_per_day"
            f.write(
f'''# HELP {metric_name} Cumulated downloaded volume by client from AUXIP per day.
# TYPE {metric_name} gauge
{metric_name}{{client="{client}"}} {event.eventDoubles[0].value}
''')
            logger.info(f"Metric {metric_name} has been generated")
        # end for
    # end if

    # CUMULATIVE_DOWNLOADED_VOLUME_PER_MONTH
    cumulative_downloaded_volume_per_month_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_VOLUME_PER_MONTH_{month_start}_{month_stop}", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_downloaded_volume_per_month_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded volume from AUXIP per month")
    else:
        event = cumulative_downloaded_volume_per_month_events[0]
        metric_name = "auxip_cumulative_downloaded_volume_per_month"
        f.write(
f'''# HELP {metric_name} Cumulated downloaded volume from AUXIP per month.
# TYPE {metric_name} gauge
{metric_name} {event.eventDoubles[0].value}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if
    
    # CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_MONTH
    cumulative_downloaded_volume_by_client_per_month_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT_PER_MONTH_{month_start}_{month_stop}", "op": "=="}
    )
    if len(cumulative_downloaded_volume_by_client_per_month_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded volume by client from AUXIP per month")
    else:
        for event in cumulative_downloaded_volume_by_client_per_month_events:
            client = event.gauge.system
            metric_name = "auxip_cumulative_downloaded_volume_by_client_per_month"
            f.write(
f'''# HELP {metric_name} Cumulated downloaded volume by client from AUXIP per month.
# TYPE {metric_name} gauge
{metric_name}{{client="{client}"}} {event.eventDoubles[0].value}
''')
            logger.info(f"Metric {metric_name} has been generated")
        # end for
    # end if

    # CUMULATIVE_DOWNLOADED_VOLUME
    cumulative_downloaded_volume_events = query.get_events(
        gauge_names = {"filter": "CUMULATIVE_DOWNLOADED_VOLUME", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_downloaded_volume_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded volume from AUXIP globally")
    else:
        event = cumulative_downloaded_volume_events[0]
        metric_name = "auxip_cumulative_downloaded_volume_globally"
        f.write(
f'''# HELP {metric_name} Cumulated downloaded volume from AUXIP globally.
# TYPE {metric_name} gauge
{metric_name} {event.eventDoubles[0].value}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if
    
    # CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT
    cumulative_downloaded_volume_by_client_events = query.get_events(
        gauge_names = {"filter": "CUMULATIVE_DOWNLOADED_VOLUME_BY_CLIENT", "op": "=="}
    )
    if len(cumulative_downloaded_volume_by_client_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded volume by client from AUXIP globally")
    else:
        for event in cumulative_downloaded_volume_by_client_events:
            client = event.gauge.system
            metric_name = "auxip_cumulative_downloaded_volume_by_client_globally"
            f.write(
f'''# HELP {metric_name} Cumulated downloaded volume by client from AUXIP globally.
# TYPE {metric_name} gauge
{metric_name}{{client="{client}"}} {event.eventDoubles[0].value}
''')
            logger.info(f"Metric {metric_name} has been generated")
        # end for
    # end if

    ##############################
    # DOWNLOADED NUMBER OF FILES #
    ##############################
    # CUMULATIVE_DOWNLOADED_NUMBER_PER_DAY
    cumulative_downloaded_number_per_day_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_NUMBER_PER_DAY_{day_start}_{day_stop}", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_downloaded_number_per_day_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded number of files from AUXIP per day")
    else:
        event = cumulative_downloaded_number_per_day_events[0]
        metric_name = "auxip_cumulative_downloaded_number_per_day"
        f.write(
f'''# HELP {metric_name} Cumulated downloaded number of files from AUXIP per day.
# TYPE {metric_name} gauge
{metric_name} {event.eventDoubles[0].value}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if
    
    # CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_DAY
    cumulative_downloaded_number_by_client_per_day_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_DAY_{day_start}_{day_stop}", "op": "=="}
    )
    if len(cumulative_downloaded_number_by_client_per_day_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded number of files by client from AUXIP per day")
    else:
        for event in cumulative_downloaded_number_by_client_per_day_events:
            client = event.gauge.system
            metric_name = "auxip_cumulative_downloaded_number_by_client_per_day"
            f.write(
f'''# HELP {metric_name} Cumulated downloaded number of files by client from AUXIP per day.
# TYPE {metric_name} gauge
{metric_name}{{client="{client}"}} {event.eventDoubles[0].value}
''')
            logger.info(f"Metric {metric_name} has been generated")
        # end for
    # end if

    # CUMULATIVE_DOWNLOADED_NUMBER_PER_MONTH
    cumulative_downloaded_number_per_month_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_NUMBER_PER_MONTH_{month_start}_{month_stop}", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_downloaded_number_per_month_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded number of files from AUXIP per month")
    else:
        event = cumulative_downloaded_number_per_month_events[0]
        metric_name = "auxip_cumulative_downloaded_number_per_month"
        f.write(
f'''# HELP {metric_name} Cumulated downloaded number of files from AUXIP per month.
# TYPE {metric_name} gauge
{metric_name} {event.eventDoubles[0].value}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if
    
    # CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_MONTH
    cumulative_downloaded_number_by_client_per_month_events = query.get_events(
        gauge_names = {"filter": f"CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT_PER_MONTH_{month_start}_{month_stop}", "op": "=="}
    )
    if len(cumulative_downloaded_number_by_client_per_month_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded number of files by client from AUXIP per month")
    else:
        for event in cumulative_downloaded_number_by_client_per_month_events:
            client = event.gauge.system
            metric_name = "auxip_cumulative_downloaded_number_by_client_per_month"
            f.write(
f'''# HELP {metric_name} Cumulated downloaded number of files by client from AUXIP per month.
# TYPE {metric_name} gauge
{metric_name}{{client="{client}"}} {event.eventDoubles[0].value}
''')
            logger.info(f"Metric {metric_name} has been generated")
        # end for
    # end if

    # CUMULATIVE_DOWNLOADED_NUMBER
    cumulative_downloaded_number_events = query.get_events(
        gauge_names = {"filter": "CUMULATIVE_DOWNLOADED_NUMBER", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_downloaded_number_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded number of files from AUXIP globally")
    else:
        event = cumulative_downloaded_number_events[0]
        metric_name = "auxip_cumulative_downloaded_number_globally"
        f.write(
f'''# HELP {metric_name} Cumulated downloaded number of files from AUXIP globally.
# TYPE {metric_name} gauge
{metric_name} {event.eventDoubles[0].value}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if
    
    # CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT
    cumulative_downloaded_number_by_client_events = query.get_events(
        gauge_names = {"filter": "CUMULATIVE_DOWNLOADED_NUMBER_BY_CLIENT", "op": "=="}
    )
    if len(cumulative_downloaded_number_by_client_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated downloaded number of files by client from AUXIP globally")
    else:
        for event in cumulative_downloaded_number_by_client_events:
            client = event.gauge.system
            metric_name = "auxip_cumulative_downloaded_number_by_client_globally"
            f.write(
f'''# HELP {metric_name} Cumulated downloaded number of files by client from AUXIP globally.
# TYPE {metric_name} gauge
{metric_name}{{client="{client}"}} {event.eventDoubles[0].value}
''')
            logger.info(f"Metric {metric_name} has been generated")
        # end for
    # end if
    
    # CUMULATIVE_DOWNLOAD_TIME
    cumulative_download_time_events = query.get_events(
        gauge_names = {"filter": "CUMULATIVE_DOWNLOAD_TIME", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_download_time_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated download time globally")
    elif len(cumulative_downloaded_number_events) > 0:
        cumulative_download_time_event = cumulative_download_time_events[0]
        cumulative_downloaded_number_event = cumulative_downloaded_number_events[0]
        average_time_to_download_files = cumulative_download_time_event.eventDoubles[0].value / cumulative_downloaded_number_event.eventDoubles[0].value
        metric_name = "auxip_average_time_to_download_files_globally"
        f.write(
f'''# HELP {metric_name} Average time to download files from AUXIP globally.
# TYPE {metric_name} gauge
{metric_name} {average_time_to_download_files}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if
    
    # CUMULATIVE_DOWNLOAD_SPEED
    cumulative_download_speed_events = query.get_events(
        gauge_names = {"filter": "CUMULATIVE_DOWNLOAD_SPEED", "op": "=="},
        gauge_systems = {"filter": "GLOBAL", "op": "=="}
    )
    if len(cumulative_download_speed_events) == 0:
        adgsboa_metrics_up = 0
        logger.error(f"There is not information about the cumulated download speed globally")
    elif len(cumulative_downloaded_number_events) > 0:
        cumulative_download_speed_event = cumulative_download_speed_events[0]
        cumulative_downloaded_number_event = cumulative_downloaded_number_events[0]
        average_speed_to_download_files = cumulative_download_speed_event.eventDoubles[0].value / cumulative_downloaded_number_event.eventDoubles[0].value
        metric_name = "auxip_average_speed_to_download_files_globally"
        f.write(
f'''# HELP {metric_name} Average speed to download files from AUXIP globally.
# TYPE {metric_name} gauge
{metric_name} {average_speed_to_download_files}
''')
        logger.info(f"Metric {metric_name} has been generated")
    # end if

    f.write(
f'''# HELP adgsboa_metrics_up Status of the generation of ADGSBOA metrics (1 is 'up', 0 otherwise).
# TYPE adgsboa_metrics_up gauge
adgsboa_metrics_up{{service_name="ADGSBOA metrics"}} {adgsboa_metrics_up}
''')
    
    f.close()

    shutil.move(temporary_file_path, metrics_file_path)

    logger.info(f"Metrics have been written to file {metrics_file_path}")
    
    return

def main():

    args_parser = argparse.ArgumentParser(description='ADGSBOA metrics generation tool.')
    args_parser.add_argument("-b", dest="begin", type=str, nargs=1,
                             help="start date of the reporting period", required=False)
    args_parser.add_argument("-e", dest="end", type=str, nargs=1,
                             help="stop date of the reporting period", required=False)
    args_parser.add_argument("-o", dest="metrics_file_path", type=str, nargs=1,
                             help="path to the output metrics file", required=True)

    args = args_parser.parse_args()
    metrics_file_path = args.metrics_file_path[0]

    # Get the timings of the window to cover
    begin = datetime.datetime.now().isoformat()
    end = datetime.datetime.now().isoformat()
    if args.begin != None:
        begin = args.begin[0]
    # end if
    if args.end != None:
        end = args.end[0]
    # end if

    if parser.parse(begin) > parser.parse(end):
        log = f"The generator {os.path.basename(__file__)} has been triggered with a begin value ({begin}) greater than the end value ({end})"
        logger.error(log)
        raise Exception(log)
    # end if

    execute_generator(begin, end, metrics_file_path)
    
    exit(0)

if __name__ == "__main__":

    main()
