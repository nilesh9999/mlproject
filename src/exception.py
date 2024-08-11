import sys
import logging

# Configure logging to write to a file
logging.basicConfig(
    filename="error.log",  # Log file name
    filemode="a",          # Append mode
    level=logging.ERROR,   # Log level
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

class CustomException(Exception):
    def __init__(self, message: str, error_detail: sys):
        super().__init__(message)
        self.message = self.get_error_message(message, error_detail)
        logging.error(self.message)  # Log the error when the exception is created
    
    def get_error_message(self, message: str, error_detail: sys) -> str:
        exc_type, exc_value, exc_tb = error_detail.exc_info()
        if exc_tb is None:
            # If traceback information is not available
            return message
        file_name = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        # Creating the error message with file path and line number
        error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] - {message}"
        return error_message

    def __str__(self):
        return self.message

def divide_numbers(a: int, b: int):
    try:
        if a == 0:
            raise CustomException("Variable 'a' should not be zero", sys)
        if b == 0:
            raise CustomException("Variable 'b' should not be zero", sys)
        
        result = a / b
        return result
    except CustomException as e:
        # Handle custom exceptions and re-raise if necessary
        print(e)
        raise
    except ZeroDivisionError as e:
        # This block might not be needed anymore if custom exceptions handle zero cases
        raise CustomException("Attempted to divide by zero", sys) from e

# Test cases
try:
    divide_numbers(0, 10)  # This will raise an exception for 'a'
except CustomException as e:
    print(e)

try:
    divide_numbers(10, 0)  # This will raise an exception for 'b'
except CustomException as e:
    print(e)
