class LoggerConfig:
    dictConfig = {
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'level': 'WARNING',
                'class': 'logging.FileHandler',
                'formatter': 'default',
                'filename': 'log/application.log',
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        }
    }

