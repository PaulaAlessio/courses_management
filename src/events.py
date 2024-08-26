from flask import (
  Blueprint,
  render_template,
)

from src.database import get_db

bp = Blueprint("events", __name__)


@bp.route("/events")
def events():
  db = get_db()
  my_events = db.execute(
    "SELECT * FROM event_type"
  ).fetchall()
  return render_template("events/events.html", events=my_events)
