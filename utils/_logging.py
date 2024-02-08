import logging
import multiprocessing


BASIC_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"


def _init_logger(name=None, level=logging.INFO):
    """初始化一个 logger
    参数说明
    -------
    name: 日志名称，为空则是用当前进程的名称
    level: must be an int or a str
        logging.ERROR = 40
        logging.WARNING = 30
        logging.WARN = WARNING
        logging.INFO = 20
    """
    if name is None:
        name = multiprocessing.current_process().name
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


def _add_handler(logger: logging.Logger, handler: logging.Handler, level=None, format: str = logging.BASIC_FORMAT):
    """给当前 logger 添加 handler
    参数说明
    -------
    logger: logging.Logger
    handler: logging.Handler
    format: 默认格式为 `%(levelname)s:%(name)s:%(message)s`
        指定为 None 时不会去设置
    """
    if level:
        handler.setLevel(level)
    if format is not None:
        handler.setFormatter(logging.Formatter(format))
    logger.addHandler(handler)


def create_console_logger(name=None, level=logging.INFO, format=None):
    """创建一个输出到控制台的 logger
    参数说明
    -------
    name: 日志名称，为空则是用当前进程的名称
    level: 默认是 info
    """
    logger = _init_logger(name)
    if format is None:
        format = BASIC_FORMAT
    _add_handler(logger, logging.StreamHandler(), level=level, format=format)
    return logger
