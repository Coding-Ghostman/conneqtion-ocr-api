import logging

def setup_logger(name = "System Logs", log_file = "system_logs.log", level=logging.INFO):
    """Function to set up a logger."""
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

val = setup_logger("mylogger")
val.info("checking stuff")
val.warning("checking other stuff")
val.error("Error mate")
val.critical("This is critical")


