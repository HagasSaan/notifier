import structlog

from configuration.models import Configuration
from notifier.celery import app

logger = structlog.get_logger(__name__)


@app.task
def run_configuration(
    configuration_id: int,
) -> None:
    logger.bind(configuration_id=configuration_id)
    try:
        configuration = Configuration.objects.get(id=configuration_id)
        configuration.run()
        logger.info('Configuration executed')
    except Exception as e:
        logger.error(
            'Configuration execution failed',
            reason=str(e),
        )
