
import sys
#import logging
from src.logger import logging

def error_message_detail(error, error_detail:sys):
    _,_,exc_tb = error_detail.exc_info()

    print(exc_tb)

    file_name = exc_tb.tb_frame.f_code.co_filename

    error_message = "Error in Python script {}, line# {}, err_msg {}".format(file_name, exc_tb.tb_frame.f_lineno, str(error))

    return error_message

class customException(Exception):
    def __init__(self, error, error_detail:sys):
        super().__init__(error)

        self.error = error_message_detail(error=error, error_detail=error_detail)

    def __str__(self):
        return self.error

if __name__ == "__main__":
    try:
        1/0
    except Exception as e:
        print('err from exception is ', e)
        logging.info("Divide by 0 error")
        raise customException(e, sys)