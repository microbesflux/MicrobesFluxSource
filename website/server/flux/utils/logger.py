import logging
class LogHandler(logging.Handler):
    def emit(self, record):
        print record.levelname, record.msg
log_handler = LogHandler()
