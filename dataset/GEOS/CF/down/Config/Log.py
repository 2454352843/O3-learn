import logging

class logg:
    def __init__(self):
        self.log = self.getLogger()

    def getLogger(self):
        # 创建Logger
        logger = logging.getLogger()
        logger.setLevel(logging.DEBUG)

        # 创建Handler

        # 终端Handler
        consoleHandler = logging.StreamHandler()
        consoleHandler.setLevel(logging.DEBUG)

        # 文件Handler
        fileHandler = logging.FileHandler('log.log', mode='w', encoding='UTF-8')
        fileHandler.setLevel(logging.NOTSET)

        # Formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s - line: %(lineno)d - %(message)s')
        consoleHandler.setFormatter(formatter)
        fileHandler.setFormatter(formatter)

        # 添加到Logger中
        logger.addHandler(consoleHandler)
        logger.addHandler(fileHandler)

        return logger

    def __get__(self, instance, owner):
        return self.log