import logging
from app.core.context import get_request_id

_LOG_FORMAT = (
    "%(asctime)s | %(levelname)s | %(name)s | "
    "request_id=%(request_id)s | %(message)s"
)

class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        request_id = get_request_id()
        record.request_id = request_id if request_id else "-"
        return True

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        handler = logging.StreamHandler()
        
        formatter = logging.Formatter(_LOG_FORMAT)
        handler.setFormatter(formatter)
        
        handler.addFilter(RequestIdFilter())
        logger.addHandler(handler)
        
    return logger