import os
from flask_migrate import Migrate
from werkzeug.serving import run_simple

from app import create_app, db

app = create_app(os.getenv("FLASK_CONFIG") or "dev")
migrate = Migrate(app, db)


if __name__ == "__main__":
    run_simple("localhost", 8000, app, use_reloader=True)

