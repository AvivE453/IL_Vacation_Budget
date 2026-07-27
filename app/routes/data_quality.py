from flask import Blueprint, render_template

from app.db import get_cursor
from app.queries import get_collection_volume, get_data_quality_report

# Groups this file's routes under one name. app/main.py registers it onto
# the actual Flask app via app.register_blueprint.
bp = Blueprint("data_quality", __name__)


# Coverage + missing-data report across all destinations.
@bp.route("/data-quality")
def index():
    with get_cursor() as cur:
        coverage = get_data_quality_report(cur)
        volume = get_collection_volume(cur)
    return render_template("data_quality.html", coverage=coverage, volume=volume)
