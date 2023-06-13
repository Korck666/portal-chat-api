# util/cleanup.py
import shutil
from typing import Optional
from pathlib import Path
from threading import Lock
import logging
import utils.config as config
from services.logger import Logger
import datetime
import os

logger = Logger()


class Cleanup:
    """
    Singleton class to handle cleanup operations
    """
    __instance = None

    def __new__(cls) -> "Cleanup":
        """
        Create a new instance of the class if it doesn't exist
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance

    def __init__(self) -> None:
        """
        Initialize the cleanup instance
        """
        if self.__initialized:
            return
        self.__initialized = True
        self.lock = Lock()
        self.config = config.Config()
        self.PYCACHE = self.config.PYCACHE
        self.root_dir = Path(self.config.WORKDIR)

    def cleanup_cache(self, root_dir: Optional[str] = None) -> None:
        """
        Recursively deletes cache folders from the specified directory or the root directory
        :param root_dir: directory to delete from
        :type root_dir: str
        """
        root: Path = Path(root_dir) if root_dir is not None else self.root_dir
        for path in root.glob('**/*'):
            if path.is_dir() and path.name == self.PYCACHE:
                logger.info(f"Deleting cache folder: {path}")
                shutil.rmtree(path)
            elif path.is_dir() and path.name.startswith('.'):
                logger.debug(f"Skipping hidden folder: {path}")

    def check_log_size(self) -> None:
        """
        Checks the size of the current log file
        """
        # check log file size and backup rules here
        logger.info("Checking log file size.")
        # check log file size and backup rules here
        if self.config.LOG_FILE_MAX_BYTES*0.99 >= Logger.filehandler.stream.tell():
            logger.warning("Log file has reached the maximum size.")
            self.close_log_file()

        logger.info("Deleting extra backup log files.")
        # delete any extra backup log files beyond the specified backup rules

    def close_log_file(self) -> None:
        """
        Closes the current log file
        """
        logger.info("Closing the current log file.")
        with self.lock:
            # when closing the log file, close the handler and open a new one
            Logger.filehandler.flush()
            Logger.filehandler.close()
            logger.removeHandler(Logger.filehandler)
            # move the log file to the backup location
            self.move_to_backup()
            Logger.new_filehandler()

    def move_to_backup(self) -> None:
        """
        Moves the current log file to backup
        """
        logger.info("Checking backup rules.")
        # TODO: check the number of backup files and delete any extra backup files

        if not os.path.exists(self.config.LOG_BACKUP_PATH):
            os.mkdir(self.config.LOG_BACKUP_PATH)
            now = datetime.datetime.now()
            timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
            backup_filename = f"{timestamp}_{self.config.LOG_FILE}"
            fromlog = f"{self.config.LOG_PATH}/{self.config.LOG_FILE}"
            tobackup = f"{self.config.LOG_BACKUP_PATH}/{backup_filename}"
            shutil.copy(fromlog, tobackup)
            logger.info(f"Moved closed log file to backup {backup_filename}")
