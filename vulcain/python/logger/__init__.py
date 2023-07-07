import sys
import logging
import socket


class HostnameFilter(logging.Filter):
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)

    def filter(self, record):
        record.hostname = HostnameFilter.hostname
        record.ip = HostnameFilter.ip
        return True


class Logger():
    def __init__(self, name="Vulcain", 
                 default_level=logging.INFO, 
                 log_format="[%(asctime)s] - [%(hostname)s][%(ip)s] - [%(name)s] - [%(levelname)s] :\n%(message)s\n", 
                 date_format="%Y-%b-%d %H:%M:%S"):
        self.LOGGER_NAME = name
        self.LEVEL_DEFAULT = default_level
        self.LOG_FORMAT = log_format
        self.DATE_FORMAT = date_format

    _logger_obj = None

    def logger_obj(self):

        if not self._logger_obj:
            if self.logger_exist():
                self._logger_obj = logging.getLogger(self.LOGGER_NAME)

            else:
                self._logger_obj = logging.getLogger(self.LOGGER_NAME)
                self._logger_obj.addFilter(HostnameFilter())
                self._logger_obj.setLevel(self.LEVEL_DEFAULT)

                fmt = logging.Formatter(self.LOG_FORMAT, self.DATE_FORMAT)

                stream_handler = logging.StreamHandler(sys.stderr)
                stream_handler.setFormatter(fmt)
                self._logger_obj.addHandler(stream_handler)

        return self._logger_obj

    def set_level(self, level):
        lg = self.logger_obj()
        lg.setLevel(level)

    def logger_exist(self):
        return self.LOGGER_NAME in logging.Logger.manager.loggerDict.keys()

    def debug(self, msg, *args, **kwargs):
        lg = self.logger_obj()
        lg.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        lg = self.logger_obj()
        lg.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        lg = self.logger_obj()
        lg.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        lg = self.logger_obj()
        lg.error(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        lg = self.logger_obj()
        lg.critical(msg, *args, **kwargs)

    def log(self, level, msg, *args, **kwargs):
        lg = self.logger_obj()
        lg.log(level, msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        lg = self.logger_obj()
        lg.exception(msg, *args, **kwargs)

    def write_to_file(self, path, level=logging.DEBUG):
        file_handler = logging.FileHandler(path)
        file_handler.setLevel(level)

        fmt = logging.Formatter(self.LOG_FORMAT, self.DATE_FORMAT)
        file_handler.setFormatter(fmt)

        lg = self.logger_obj()
        lg.addHandler(file_handler)


if __name__ == "__main__":

    logger = Logger(name="MyLogger")
    logger.write_to_file("D:\PROJETS\gen\log\something.log")
    logger.LEVEL_DEFAULT = logging.INFO
    logger.debug("debug message")
    logger.info("info message")
    logger.warning("warning message")
    logger.error("error message")
    logger.critical("critical message")

    """
    try:
        a = []
        b = a[0]
    except:
        logger.exception("Exception message")
    """