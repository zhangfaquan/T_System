#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: record
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for handling video records of T_System.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from t_system import log_manager
from t_system import record_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def get_record_dates(admin_id):
    """Method to return existing positions.

    Args:
        admin_id (str):                 Root privileges flag.
    """
    try:
        result = record_manager.get_record_dates()
    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_records(admin_id, records_date):
    """Method to return existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        records_date (str):             Date of the wanted records.
    """
    result = []

    try:
        records = record_manager.get_records(records_date)

        if records:
            for record in records:
                result.append({"id": record.id, "name": record.name, "time": record.time, "length": record.length})

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_record(admin_id, record_id):
    """Method to return existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        record_id (str):                The id of the record.
    """
    try:

        record = record_manager.get_record(record_id)

        if not record:
            result = ""
        else:

            result = record.merged_file

    except Exception as e:
        logger.error(e)
        result = ""

    return result


def update_record(admin_id, record_id, data):
    """Method to remove existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        record_id (str):                The id of the record.
    """

    result = record_manager.update_record(record_id, data["name"])

    return result


def delete_record(admin_id, record_id):
    """Method to remove existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        record_id (str):                The id of the record.
    """

    result = record_manager.delete_record(record_id)

    return result