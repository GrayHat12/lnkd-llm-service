from logging.config import dictConfig
from logging import getLogger
from config.app_config import CORE_STAGE_KEY
import os

def configure_logging() -> None:
    dictConfig(
        {
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {  # correlation ID filter must be added here to make the %(correlation_id)s formatter work
                'correlation_id': {
                    '()': 'asgi_correlation_id.CorrelationIdFilter',
                    'uuid_length': 8 if not os.environ[CORE_STAGE_KEY] == 'LOCAL' else 32,
                    'default_value': '-',
                },
            },
            'formatters': {
                'console': {
                    'class': 'logging.Formatter',
                    'datefmt': '%Y-%m-%d %H:%M:%S',
                    # formatter decides how our console logs look, and what info is included.
                    # adding %(correlation_id)s to this format is what make correlation IDs appear in our logs
                    'format': '%(levelname)s:\t  %(asctime)s -  %(name)s:%(lineno)d -  [%(correlation_id)s] -  %(message)s',
                },
            },
            'handlers': {
                'console': {
                    'class': 'logging.StreamHandler',
                    # Filter must be declared in the handler, otherwise it won't be included
                    'filters': ['correlation_id'],
                    'formatter': 'console',
                },
            },
            # Loggers can be specified to set the log-level to log, and which handlers to use
            'loggers': {
                # project logger
                '[LnkdIn-LLM-BFF]': {'handlers': ['console'], 'level': 'DEBUG', 'propagate': True},
                # third-party package loggers
                'databases': {'handlers': ['console'], 'level': 'WARNING'},
                'httpx': {'handlers': ['console'], 'level': 'INFO'},
                'asgi_correlation_id': {'handlers': ['console'], 'level': 'WARNING'},
            },
        }
    )

configure_logging()
logger = getLogger('[LnkdIn-LLM-BFF]')