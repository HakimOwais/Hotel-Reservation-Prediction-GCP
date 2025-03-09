from source.custom_logger import get_logger
from source.custom_exception import CustomException

import sys

logger = get_logger(__name__)

def divide_number(a,b):
    try:
        result = a/b
        logger.info("Dividing two numbers")
        return result
    except Exception as e:
        logger.error("Error message")
        raise CustomException("Custom error ", sys)
    


if __name__ == "__main__":
    try:
        logger.info("STARTING the program")
        divide_number(10,0)

    except CustomException as ce:
        logger.error(str(ce))