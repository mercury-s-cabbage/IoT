import logging

class ColorFormatter(logging.Formatter):
    # ANSI escape sequences для цветов
    GREY = "\x1b[90m"
    BLUE = "\x1b[94m"
    RED = "\x1b[91m"
    YELLOW = "\x1b[93m"
    RESET = "\x1b[0m"

    FORMATS = {
        logging.DEBUG: GREY + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.INFO: BLUE + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.WARNING: YELLOW + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.ERROR: RED + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
        logging.CRITICAL: RED + "%(asctime)s - %(levelname)s - %(message)s" + RESET,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS[logging.INFO])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

def setup_logger(log_file='bot.log'):
    logger = logging.getLogger('DungeonBot')
    logger.setLevel(logging.DEBUG)

    # Логирование в файл (без цвета)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    # Логирование в консоль с цветом
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(ColorFormatter())

    # Добавляем обработчики, если они ещё не добавлены (чтобы не дублировать при повторном импорте)
    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger
