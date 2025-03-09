import logging  # Importing the logging module for logging messages.
import os  # Importing the os module to handle file and directory operations.
from datetime import datetime  # Importing datetime to generate timestamps for log files.

# Define the directory where log files will be stored.
LOGS_DIR = "logs"
# Create the logs directory if it does not exist.
os.makedirs(LOGS_DIR, exist_ok=True)

# Define the log file name with the current date appended.
LOG_FILE = os.path.join(LOGS_DIR, f"log_{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure the logging settings.
logging.basicConfig(
    filename=LOG_FILE,  # Set the filename for log output.
    format='%(asctime)s - %(levelname)s - %(message)s',  # Define the log message format.
    level=logging.INFO  # Set the logging level to INFO.
)

def get_logger(name):
    """
    Returns a logger instance with the specified name.
    
    Args:
        name (str): The name of the logger.
    
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)  # Create a logger with the given name.
    logger.setLevel(logging.INFO)  # Set the logger level to INFO.
    return logger  # Return the logger instance.
