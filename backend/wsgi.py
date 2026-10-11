import os
import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
logger = logging.getLogger("clauseguard.wsgi")

backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

port = os.environ.get("PORT", "5000")
logger.info(f"Starting ClauseGuard AI WSGI on port {port}...")

from app import create_app
from app.extensions import db

app = create_app()
logger.info("ClauseGuard AI application initialized successfully and ready for traffic!")

if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    app.run(host="0.0.0.0", port=int(port), debug=debug)
