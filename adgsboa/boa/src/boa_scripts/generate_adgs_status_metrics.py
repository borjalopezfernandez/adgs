#!/usr/bin/env python3
"""
Tool for generating ADGS status metrics for prometheus

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
import shlex
from subprocess import Popen, PIPE
import requests

# Import logging
from eboa.logging import Log

logging = Log(name = __name__, log_name = "eboa_metrics_root_operations.log")
logger = logging.logger

def execute_command(command):
    """
    Method to execute commands
    
    :param command: command to execute inside the mutex
    :type command: str
    """
    exit_code = 0
    command_split = shlex.split(command)
    program = Popen(command_split, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    output, error = program.communicate()
    return_code = program.returncode

    return output, error, return_code

def execute_generator(metrics_file_path):
    """Function to generate the metrics from the ADGSBOA
    
    :param metrics_file_path: path to the output metrics file
    :type metrics_file_path: str
    """

    logger.info(f"Generating ADGS status metrics to path {metrics_file_path}")
    
    # Temporary file is moved to the final destination once closed
    temporary_file = tempfile.NamedTemporaryFile(delete=False)
    temporary_file_path = temporary_file.name

    f= open(temporary_file_path,"w+")

    services = {}
    ##########
    # minArc #
    ##########
    service_name = "adgs_minarc"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS archive"
    }
    check_service_command = f"docker inspect -f '{{{{.State.Running}}}}' {service_name}"
    output, error, return_code = execute_command(check_service_command)
    if return_code != 0:
        services[service_name]["status"] = 0
        logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
    elif output.decode("UTF-8").replace("\n", "") != "true":
        services[service_name]["status"] = 0
        logger.error(f"The service {service_name} is not running. Checked with the execution of the command: {check_service_command}")
    else:
        check_service_command = f"docker top {service_name}"
        output, error, return_code = execute_command(check_service_command)
        if return_code != 0:
            services[service_name]["status"] = 0
            logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
        # elif "postgres" not in output.decode("UTF-8"):
        #     services[service_name]["status"] = 0
        #     logger.error(f"There are no postgres processes running in the container associated to the service {service_name}. Checked with the execution of the command: {check_service_command}")
        # end if
    # end if

    #######
    # DEC #
    #######
    service_name = "adgs_dec"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS circulator"
    }
    check_service_command = f"docker inspect -f '{{{{.State.Running}}}}' {service_name}"
    output, error, return_code = execute_command(check_service_command)
    if return_code != 0:
        services[service_name]["status"] = 0
        logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
    elif output.decode("UTF-8").replace("\n", "") != "true":
        services[service_name]["status"] = 0
        logger.error(f"The service {service_name} is not running. Checked with the execution of the command: {check_service_command}")
    else:
        check_service_command = f"docker top {service_name}"
        output, error, return_code = execute_command(check_service_command)
        if return_code != 0:
            services[service_name]["status"] = 0
            logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
        # elif "postgres" not in output.decode("UTF-8"):
        #     services[service_name]["status"] = 0
        #     logger.error(f"There are no postgres processes running in the container associated to the service {service_name}. Checked with the execution of the command: {check_service_command}")
        # end if
    # end if

    #############
    # ADGS DDBB #
    #############
    service_name = "adgs_db"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS DDBB"
    }
    check_service_command = f"docker inspect -f '{{{{.State.Running}}}}' {service_name}"
    output, error, return_code = execute_command(check_service_command)
    if return_code != 0:
        services[service_name]["status"] = 0
        logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
    elif output.decode("UTF-8").replace("\n", "") != "true":
        services[service_name]["status"] = 0
        logger.error(f"The service {service_name} is not running. Checked with the execution of the command: {check_service_command}")
    else:
        check_service_command = f"docker top {service_name}"
        output, error, return_code = execute_command(check_service_command)
        if return_code != 0:
            services[service_name]["status"] = 0
            logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
        elif "postgres" not in output.decode("UTF-8"):
            services[service_name]["status"] = 0
            logger.error(f"There are no postgres processes running in the container associated to the service {service_name}. Checked with the execution of the command: {check_service_command}")
        # end if
    # end if

    ############
    # BOA DDBB #
    ############
    service_name = "adgs_monitoring_ddbb"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS monitoring DDBB"
    }
    check_service_command = f"docker inspect -f '{{{{.State.Running}}}}' {service_name}"
    output, error, return_code = execute_command(check_service_command)
    if return_code != 0:
        services[service_name]["status"] = 0
        logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
    elif output.decode("UTF-8").replace("\n", "") != "true":
        services[service_name]["status"] = 0
        logger.error(f"The service {service_name} is not running. Checked with the execution of the command: {check_service_command}")
    else:
        check_service_command = f"docker top {service_name}"
        output, error, return_code = execute_command(check_service_command)
        if return_code != 0:
            services[service_name]["status"] = 0
            logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
        elif "postgres" not in output.decode("UTF-8"):
            services[service_name]["status"] = 0
            logger.error(f"There are no postgres processes running in the container associated to the service {service_name}. Checked with the execution of the command: {check_service_command}")
        # end if
    # end if

    ########
    # VBOA #
    ########
    service_name = "adgs_boa"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS BOA"
    }
    check_service_command = f"docker inspect -f '{{{{.State.Running}}}}' {service_name}"
    output, error, return_code = execute_command(check_service_command)
    if return_code != 0:
        services[service_name]["status"] = 0
        logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
    elif output.decode("UTF-8").replace("\n", "") != "true":
        services[service_name]["status"] = 0
        logger.error(f"The service {service_name} is not running. Checked with the execution of the command: {check_service_command}")
    else:
        check_service_command = f"docker top {service_name}"
        output, error, return_code = execute_command(check_service_command)
        if return_code != 0:
            services[service_name]["status"] = 0
            logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
        elif ("flask" not in output.decode("UTF-8")) and not ("gunicorn" not in output.decode("UTF-8")):
            services[service_name]["status"] = 0
            logger.error(f"There are no flask or gunicorn processes running in the container associated to the service {service_name}. Checked with the execution of the command: {check_service_command}")
        # end if
    # end if

    #############
    # ORC (BOA) #
    #############
    service_name = "adgs_orc_boa"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS orchestrator for BOA"
    }
    # Request status for ORC and minArc services inside BOA
    orc_minarc_boa_status_url = "http://localhost:5000/check-orc-status"
    orc_minarc_boa_status = requests.get(orc_minarc_boa_status_url)
    if orc_minarc_boa_status.status_code != 200:
        services[service_name]["status"] = 0
        logger.error(f"The request ({orc_minarc_boa_status_url}) to get the status of ORC (BOA) has failed with the following code: {response.status_code}")
    else:
        if orc_minarc_boa_status.json()["scheduler"]["status"] != "on":
            services[service_name]["status"] = 0
            logger.error(f"There is no ORC scheduler process running in the container associated to the service {service_name}. Checked with the execution of the request to the url: {orc_minarc_boa_status_url}")
        # end if
    # end if

    ################
    # minArc (BOA) #
    ################
    service_name = "adgs_minarc_boa"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS archive for BOA"
    }
    if orc_minarc_boa_status.status_code != 200:
        services[service_name]["status"] = 0
        logger.error(f"The request ({orc_minarc_boa_status_url}) to get the status of ORC (BOA) has failed with the following code: {response.status_code}")
    else:
        if orc_minarc_boa_status.json()["ingester"]["status"] != "on":
            services[service_name]["status"] = 0
            logger.error(f"There is no ORC scheduler process running in the container associated to the service {service_name}. Checked with the execution of the request to the url: {orc_minarc_boa_status_url}")
        # end if
    # end if

    ###########
    # grafana #
    ###########
    service_name = "adgs_grafana"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS Grafana"
    }
    check_service_command = f"docker inspect -f '{{{{.State.Running}}}}' {service_name}"
    output, error, return_code = execute_command(check_service_command)
    if return_code != 0:
        services[service_name]["status"] = 0
        logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
    elif output.decode("UTF-8").replace("\n", "") != "true":
        services[service_name]["status"] = 0
        logger.error(f"The service {service_name} is not running. Checked with the execution of the command: {check_service_command}")
    else:
        check_service_command = f"docker top {service_name}"
        output, error, return_code = execute_command(check_service_command)
        if return_code != 0:
            services[service_name]["status"] = 0
            logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
        elif "grafana" not in output.decode("UTF-8"):
            services[service_name]["status"] = 0
            logger.error(f"There are no grafana processes running in the container associated to the service {service_name}. Checked with the execution of the command: {check_service_command}")
        # end if
    # end if

    ##############
    # prometheus #
    ##############
    service_name = "adgs_prometheus"
    services[service_name] = {
        "metric_name": f"{service_name}_up",
        "status": 1,
        "pretty_name": "ADGS Prometheus"
    }
    check_service_command = f"docker inspect -f '{{{{.State.Running}}}}' {service_name}"
    output, error, return_code = execute_command(check_service_command)
    if return_code != 0:
        services[service_name]["status"] = 0
        logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
    elif output.decode("UTF-8").replace("\n", "") != "true":
        services[service_name]["status"] = 0
        logger.error(f"The service {service_name} is not running. Checked with the execution of the command: {check_service_command}")
    else:
        check_service_command = f"docker top {service_name}"
        output, error, return_code = execute_command(check_service_command)
        if return_code != 0:
            services[service_name]["status"] = 0
            logger.error(f"The execution of the command {check_service_command} has ended unexpectedly with the following output: {output} but the following error: {error}")
        elif "prometheus" not in output.decode("UTF-8"):
            services[service_name]["status"] = 0
            logger.error(f"There are no prometheus processes running in the container associated to the service {service_name}. Checked with the execution of the command: {check_service_command}")
        # end if
    # end if

    for service_name in services:
        metric_name = services[service_name]["metric_name"]
        service_status = services[service_name]["status"]
        pretty_name = services[service_name]["pretty_name"]
        f.write(
f'''# HELP {metric_name} Status of service {service_name} (1 is 'up', 0 otherwise).
# TYPE {metric_name} gauge
{metric_name}{{service_name="{pretty_name}"}} {service_status}
''')
    # end for
    
    f.close()

    shutil.move(temporary_file_path, metrics_file_path)
    # Give read permissions for group and others
    os.chmod(metrics_file_path, 0o644)

    logger.info(f"Metrics have been written to file {metrics_file_path}")
    
    return

def main():

    args_parser = argparse.ArgumentParser(description='ADGSBOA metrics generation tool.')
    args_parser.add_argument("-o", dest="metrics_file_path", type=str, nargs=1,
                             help="path to the output metrics file", required=True)

    args = args_parser.parse_args()
    metrics_file_path = args.metrics_file_path[0]

    execute_generator(metrics_file_path)
    
    exit(0)

if __name__ == "__main__":

    main()
