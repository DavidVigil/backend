import logging as log

class Logger:
    def __init__(self, log_file='api_apps.log', level=log.INFO): #
        log.basicConfig( # 
            level=level, #Nivel de loggeo
            format='%(asctime)s:%(levelname)s [%(filename)s:%(lineno)s] %(message)s', 
            datefmt='%I:%M:%S %p', 
            handlers=[ 
                log.FileHandler(log_file), # comma added
                log.StreamHandler() 
            ]
        )
        self.logger = log

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message): # into -> info
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

if __name__=='__main__': 
    logger = Logger()
    logger.debug('Message level: DEBUG')
    logger.info('Message level: INFO')
    logger.warning('Message level: WARNING')
    logger.error('Message level: ERROR')
    logger.critical('Message level: CRITICAL')