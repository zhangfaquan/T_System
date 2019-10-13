#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
.. module:: position
    :platform: Unix
    :synopsis: the top-level submodule of T_System's remote_ui that contains the functions for managing of t_system's arm.

.. moduleauthor:: Cem Baybars GÜÇLÜ <cem.baybars@gmail.com>
"""

from tinydb import Query  # TinyDB is a lightweight document oriented database

from t_system.db_fetching import DBFetcher
from t_system.motion.action import Position
from t_system.administration import is_admin

from t_system import dot_t_system_dir, T_SYSTEM_PATH
from t_system import log_manager

logger = log_manager.get_logger(__name__, "DEBUG")


def create_position(admin_id, db_name, data):
    """Method to create new position.

    Args:
        admin_id (str):                 Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        data (dict):                    Position data structure.
    """

    # table = get_db_table(admin_id)

    position = Position(name=data['name'], cartesian_coords=data['cartesian_coords'], polar_params=data['polar_params'], root=is_admin(admin_id), db_name=db_name)

    try:
        result = True
        position_id = position.id
    except Exception:
        result = False
        position_id = None

    return result, position_id


def get_positions(admin_id, db_name):
    """Method to return existing positions.

    Args:
        admin_id (str):                 Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
    """
    try:
        table = get_db_table(is_admin(admin_id), db_name)

        result = table.all()  # result = positions

    except Exception as e:
        logger.error(e)
        result = []

    return result


def get_position(admin_id, db_name, position_id):
    """Method to return existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        position_id (str):              The id of the position.
    """
    try:
        table = get_db_table(is_admin(admin_id), db_name)

        position = table.search((Query().id == position_id))

        if not position:
            result = []
        else:
            # result = [b.to_dict() for b in record]
            result = [position[0]]

    except Exception as e:
        logger.error(e)
        result = []

    return result


def update_position(admin_id, db_name, position_id, data):
    """Method to update the position that is recorded in database with given parameters.

    Args:
        admin_id (str):                 Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        position_id (str):              The id of the position.
        data (dict):                    Position data structure.
    """
    table = get_db_table(is_admin(admin_id), db_name)

    position = table.search((Query().id == position_id))

    if not position:
        result = False
    else:
        try:

            table.update({'name': data['name'], 'cartesian_coords': data['cartesian_coords'], 'polar_coords': data['polar_coords']}, Query().id == position_id)
            result = True
        except Exception:
            result = False

    return result


def delete_position(admin_id, db_name, position_id):
    """Method to remove existing position with given id.

    Args:
        admin_id (str):                 Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
        position_id (str):              The id of the position.
    """
    table = get_db_table(is_admin(admin_id), db_name)

    if table.search((Query().id == position_id)):
        table.remove((Query().id == position_id))

        result = True
    else:
        result = False

    return result


def get_db_table(is_admin, db_name):
    """Method to set work database by root.

    Args:
        is_admin (bool):                 Root privileges flag.
        db_name (str):                  Name of the registered Database. It uses if administration privileges activated.
    """
    table = "positions"
    if is_admin:
        db_folder = f'{T_SYSTEM_PATH}/motion/action'
        return DBFetcher(db_folder, db_name, table).fetch()
    else:
        db_folder = dot_t_system_dir
        db_name = 'missions'
        return DBFetcher(db_folder, db_name, table).fetch()
