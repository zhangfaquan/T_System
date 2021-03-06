#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: logging
    :platform: Unix
    :synopsis: the top-level submodule of T_System that contains the functions and classes related to T_System's log management ability.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

import logging
import os  # Miscellaneous operating system interfaces

from t_system import dot_t_system_dir


class LogManager:
    """Class to define a log manager to log keeping ability of t_system.

    This class provides necessary initiations and functions named :func:`t_system.logging.LogManager.get_logger`
    for return specific logger for the module who called it.
    """

    def __init__(self, args):
        """Initialization method of :class:`t_system.logging.LogManager` class.

        Args:
            args:                   Command-line arguments.
        """

        self.verbose = args["verbose"]
        self.environment = args["environment"]

        self.log_folder = f'{dot_t_system_dir}/logs'

        self.__check_folders()

        self.log_filename = "logfile.log"
        self.log_file = f'{self.log_folder}/{self.log_filename}'

    class Logger:
        """Class to define a logger for handling python's logging module to the LogManager of t_system.

        This class provides necessary initiations and functions named :func:`t_system.logging.LogManager.get_logger`
        for return specific logger for the module who called it.
        """

        def __init__(self, log_manager, caller_name, level):
            """Initialization method of :class:`t_system.logging.LogManager.Logger` class.

            Args:
                log_manager:            The LogManager object.
                caller_name:            The name who called the logger.
                level:                  Level of logging. either `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`.
            """

            self.root_system = log_manager

            self.caller_name = caller_name
            self.level = self.__get_level(level)

            self.logger = logging.getLogger(self.caller_name)

            self.__set_logger()

            self.debug = self.logger.debug
            self.info = self.logger.info
            self.warning = self.logger.warning
            self.error = self.logger.error
            self.critical = self.logger.critical

        def __set_logger(self):
            """Method to setting logging logger.
            """

            self.logger.setLevel(self.level)
            self.logger.propagate = self.__get_propagate()

            file_handler, console_handler = self.__get_handlers()

            if file_handler:
                self.logger.addHandler(file_handler)

            if console_handler:
                self.logger.addHandler(console_handler)

        @staticmethod
        def __get_level(level):
            """Method to setting level of logger with given level parameter.

            Args:
                level:                  Level of logging. either `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`.
            """

            if level == "DEBUG":
                return logging.DEBUG
            elif level == "INFO":
                return logging.INFO
            elif level == "WARNING":
                return logging.WARNING
            elif level == "ERROR":
                return logging.ERROR
            elif level == "CRITICAL":
                return logging.CRITICAL
            else:
                raise Exception(f'{level} is not valid level type')

        def __get_propagate(self):
            """Method to get propagate of logger for setting activation status of the writing logs.
            """

            if self.root_system.environment == "production":
                return False
            return True

        def __get_handlers(self):
            """Method to get handler for writing logs to the file and the console.
            """

            file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

            file_handler = logging.FileHandler(self.root_system.log_file)
            file_handler.setLevel(self.level)
            file_handler.setFormatter(file_formatter)

            if self.root_system.verbose:
                console_formatter = logging.Formatter(' * %(levelname)s - %(name)s - %(message)s')

                console_handler = logging.StreamHandler()
                console_handler.setLevel(self.level)
                console_handler.setFormatter(console_formatter)

            else:
                console_handler = None

            return file_handler, console_handler

    def get_logger(self, caller_name, level):
        """Method to create a Logger object with given parameters.

        Args:
            caller_name:            The name who called the logger.
            level:                  Level of logging. either `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`.

        Returns:
            Logger: A Logger object.
        """

        return self.Logger(self, caller_name, level)

    def clear_logs(self):
        """Method to remove log file.
        """

        open(self.log_file, "w").close()

        return True

    def get_logfile(self):
        """Method to get path and name of logfile.
        """

        return self.log_file, self.log_filename

    def __check_folders(self):
        """Method to checking the necessary folders created before. If not created creates them.
        """

        if not os.path.exists(self.log_folder):
            os.mkdir(self.log_folder)
