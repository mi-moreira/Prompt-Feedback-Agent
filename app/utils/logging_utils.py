import logging
import json
from datetime import datetime

logger = logging.getLogger("morphia_agent")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter("%(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def log_event(event_type: str, **kwargs):
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event_type,
        **kwargs,
    }
    logger.info(json.dumps(payload, ensure_ascii=False))