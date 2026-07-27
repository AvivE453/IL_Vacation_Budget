# Anonymous per-browser session id -- not authentication, just a random
# UUID stored in Flask's signed session cookie (30-day lifetime, see
# app/main.py) so /history can scope results to one browser without any
# login. Shared by app/routes/estimate.py (writes it onto each search) and
# app/routes/history.py (filters by it).

import uuid

from flask import session


def get_session_id():
    if "session_id" not in session:
        session["session_id"] = str(uuid.uuid4())
        session.permanent = True
    return session["session_id"]
