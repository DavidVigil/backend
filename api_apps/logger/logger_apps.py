import logging as log

class Logger:
    def _init_(self,log_file='api_apps.log', level=log.INFO):
        log.basicConfing(
            level=level, #Nivel de loggeo
            format='%(asctime)s:%(levelname)s [%(filename)s:%(lineao)s] %(message)s', 
            datefmt='%I:%M:%S %p', 
            handlers=[ 
                log.FileHandler(log_file)
                log.StreamHandler() 
            ]
        )
        self.logger = log.getLogger()


    def debug(self, message):
        self.logger.debug(message)

    def into(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)
