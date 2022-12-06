import signal
import time


class TestFuncForTimeOut:

    @staticmethod
    def loop(duration=30):
        for i in range(duration):
            time.sleep(1)


class TimeOutException(Exception):
    day = 0
    order = 0


# https://stackoverflow.com/questions/492519/timeout-on-a-function-call
class TimeOut:
    # Register an handler for the timeout
    @staticmethod
    def handler(signum, frame):
        from web_crawler import logger
        logger.warning("time out handler is called")
        raise TimeOutException("time out")

    @staticmethod
    def timeout_click(logger, element, timeout_duration=10):
        logger.debug("timeout_click is called")
        # Register the signal function handler
        signal.signal(signal.SIGALRM, TimeOut.handler)

        # Define a timeout for your function
        logger.debug("timeout alarm is set: %s seconds", timeout_duration)
        signal.alarm(timeout_duration)

        try:
            element.click()
        finally:
            logger.debug("timeout is reset")
            signal.alarm(0)

    @staticmethod
    def timeout_func(logger, func, args=(), kwargs=None, timeout_duration=10, sleep_time=0):
        logger.debug("timeout_func is called")
        if kwargs is None:
            kwargs = {}

        # set the timeout handler
        signal.signal(signal.SIGALRM, TimeOut.handler)
        logger.debug("timeout alarm is set: %s seconds", timeout_duration)
        signal.alarm(timeout_duration)
        try:
            if sleep_time != 0:
                logger.debug("timeout is sleeping for %d seconds", sleep_time)
                time.sleep(sleep_time)
            result = func(*args, **kwargs)
        finally:
            logger.debug("timeout is reset")
            signal.alarm(0)
        return result

