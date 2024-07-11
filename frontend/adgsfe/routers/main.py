"""
Defintion of the main routers for the ADGS Front-End application

module adgsfe
"""
# Import python utilities
import os

# Import flask utilities
from flask import Blueprint, flash, current_app, render_template

# Import definition of errors
from . import errors

bp = Blueprint("main", __name__, url_prefix="/")

adgs_dashboard_url = None
if "ADGS_DASHBOARD_URL" in os.environ:
    # Get url to access ADGS Grafana
    adgs_dashboard_url = os.environ["ADGS_DASHBOARD_URL"]
else:
    raise errors.EnvironmentVariableNotDefined("The environment variable ADGS_DASHBOARD_URL is not defined")
# end if

auxip_swagger_url = None
if "AUXIP_SWAGGER_URL" in os.environ:
    # Get url to access the Swagger of the AUXIP
    auxip_swagger_url = os.environ["AUXIP_SWAGGER_URL"]
else:
    raise errors.EnvironmentVariableNotDefined("The environment variable AUXIP_SWAGGER_URL is not defined")
# end if

adgsboa_url = None
if "ADGSBOA_URL" in os.environ:
    # Get url to access ADGSBOA
    adgsboa_url = os.environ["ADGSBOA_URL"]
else:
    raise errors.EnvironmentVariableNotDefined("The environment variable ADGSBOA_URL is not defined")
# end if

adgs_metrics_manager_url = None
if "ADGS_METRICS_MANAGER_URL" in os.environ:
    # Get url to access ADGS Prometheus
    adgs_metrics_manager_url = os.environ["ADGS_METRICS_MANAGER_URL"]
else:
    raise errors.EnvironmentVariableNotDefined("The environment variable ADGS_METRICS_MANAGER_URL is not defined")
# end if

adgsdoc_url = None
if "ADGSDOC_URL" in os.environ:
    # Get url to access ADGSDOC
    adgsdoc_url = os.environ["ADGSDOC_URL"]
else:
    raise errors.EnvironmentVariableNotDefined("The environment variable ADGSDOC_URL is not defined")
# end if

@bp.route("/services", methods=["GET"])
@bp.route("/", methods=["GET"])
def show_services():
    """
    Panel with the access to the services of the ADGS
    """

    metadata = {
        "adgs_dashboard_url": adgs_dashboard_url,
        "auxip_swagger_url": auxip_swagger_url,
        "adgsboa_url": adgsboa_url,
        "adgs_metrics_manager_url": adgs_metrics_manager_url,
        "adgsdoc_url": adgsdoc_url,
    }
    
    return render_template("panel/services.html", metadata=metadata)

@bp.route("/contact", methods=["GET"])
def show_contact():
    """
    Panel with the contact point of the ADGS service
    """
    return render_template("panel/contact.html")
