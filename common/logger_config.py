import logging


def logger_config(logger_name, log_folder, log_file_name):
    """
    Configure logger for the application.

    Args:
    - log_folder (str): Path to the log folder.
    - file_name (str): Name of the log file.

    Returns:
    logging.Logger: Configured logger object.
    """
    log_path = os.path.join(logger_name, log_folder, log_file_name)
    logging.basicConfig(
        level = logging.INFO,
        format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers = [
            logging.FileHandler(log_path),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(logger_name)
