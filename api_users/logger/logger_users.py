import logging as log

class Logger:
    def __init__(self, log_file='api_users.log', level=log.INFO):
        log.basicConfig(
            level=level,
            # ordenado por fecha y hora, nivel de error, nombre del archivo y linea de código
            # para buenas prácticas
            # aquí mandamos a imprimir en que archivo y linea ocurrió el error
            format='%(asctime)s: %(levelname)s [%(filename)s:%(lineno)s] %(message)s',
            # formato gringo
            datefmt='%I:%M:%S %p',
            handlers=[
                log.FileHandler(log_file),
                log.StreamHandler()
            ]
        )
        self.logger = log


    def debug(self, message):
        self.logger.debug(message)
   
    def info(self, message):
        self.logger.info(message)
   
    def warning(self, message):
        self.logger.warning(message)


    def error(self, message):
        self.logger.error(message)
   
    def critical(self, message):
        self.logger.critical(message)


