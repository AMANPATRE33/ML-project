import logging
import os
import sys
from datetime import datetime

# 1. GENERATE LOG FILE NAME AND PATH
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(os.path.dirname(logs_path), exist_ok=True)

# 2. CONFIGURE LOGGING TO BOTH FILE AND TERMINAL
logging.basicConfig(
    level=logging.INFO,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(logs_path),      # Saves to the logs folder
        logging.StreamHandler(sys.stdout)   # Prints to VS Code Terminal
    ]
)

# 3. DETAILED ERROR MESSAGE CAPTURE
def error_message_detail(error, error_detail: sys):
    """Returns filename, line number, and error message"""
    _, _, exc_tb = error_detail.exc_info()
    file_name = exc_tb.tb_frame.f_code.co_filename
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message [{2}]".format(
        file_name, exc_tb.tb_lineno, str(error)
    )
    return error_message

# 4. CUSTOM EXCEPTION CLASS
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail=error_detail)
        # Automatically logs every exception raised
        logging.error(self.error_message)

    def __str__(self):
        return self.error_message

# Initial trigger to confirm it's working
if __name__ == "__main__":
    logging.info("Logging has started!")