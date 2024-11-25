import logging as log

class Logger:
    def __init__(self, log_file='api_apps.log', level=log.INFO):
        # Set up the logging system with basic configurations
        log.basicConfig(
            level=level,  # Define the logging level (INFO, DEBUG, etc.)
            format='%(asctime)s:%(levelname)s [%(filename)s:%(lineno)s] %(message)s',  # Format for log messages
            datefmt='%I:%M:%S %p',  # Format for the timestamp in log messages
            handlers=[  # Handlers determine where logs are sent
                log.FileHandler(log_file),  # Save logs to a file
                log.StreamHandler()  # Print logs to the console
            ]
        )
        self.logger = log.getLogger()  # Create a logger object

    # Log a debug message
    def debug(self, message):
        self.logger.debug(message, stacklevel=2)

    # Log an info message
    def info(self, message):
        self.logger.info(message, stacklevel=2)

    # Log a warning message
    def warning(self, message):
        self.logger.warning(message, stacklevel=2)

    # Log an error message
    def error(self, message):
        self.logger.error(message, stacklevel=2)

    # Log a critical message
    def critical(self, message):
        self.logger.critical(message, stacklevel=2)

# Example usage of the Logger class
if __name__ == '__main__': 
    logger = Logger()  # Initialize the Logger class
    logger.debug('Message level: DEBUG')  # Log a debug-level message
    logger.info('Message level: INFO')  # Log an info-level message
    logger.warning('Message level: WARNING')  # Log a warning-level message
    logger.error('Message level: ERROR')  # Log an error-level message
    logger.critical('Message level: CRITICAL')  # Log a critical-level message
