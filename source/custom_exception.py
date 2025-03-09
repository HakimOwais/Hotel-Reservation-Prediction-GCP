import traceback
import sys

class CustomException(Exception):
    def __init__(self, error_message, error_detail):
        """
        Custom exception class to capture detailed error messages.

        Args:
            error_message (str): The error message.
            error_detail (tuple): sys.exc_info() containing exception details.
        """
        super().__init__(error_message)
        self.error_message = self.get_detailed_error_message(error_message, error_detail)

    @staticmethod
    def get_detailed_error_message(error_message, error_detail):
        """
        Generate a detailed error message with file name and line number.

        Args:
            error_message (str): The error message.
            error_detail (tuple): sys.exc_info() containing exception details.

        Returns:
            str: Formatted error message with file name and line number.
        """
        _, _, exc_tb = error_detail  # Unpack sys.exc_info()

        file_name = exc_tb.tb_frame.f_code.co_filename  # Extract file name
        line_number = exc_tb.tb_lineno  # Extract line number

        return f"Error occurred in {file_name}, line {line_number}: {error_message}"

    def __str__(self):
        """
        Returns the formatted error message when the exception is printed.
        """
        return self.error_message
