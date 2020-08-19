import celery
import structlog

logger = structlog.get_logger(__name__)


@celery.task
def run_configuration() -> None:
    logger.info('stub in tasks, config')
