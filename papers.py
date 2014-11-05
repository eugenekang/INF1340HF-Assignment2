#!/usr/bin/env python3

""" Computer-based immigration office for Kanadia """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import re
import datetime
import json


def decide(input_file, watchlist_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains country data, such as whether
        an entry or transit visa is required, and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept", "Reject", "Secondary", and "Quarantine"
    """

    # open files, convert files to python style
    with open(input_file, "r") as input_reader:
        input_contents = input_reader.read()
        input_contents = json.loads(input_contents)
    with open(watchlist_file, "r") as watchlist_reader:
        watchlist_contents = watchlist_reader.read()
        watchlist_contents = json.loads(watchlist_contents)
    with open(countries_file, "r") as countries_reader:
       countries_contents = countries_reader.read()
       countries_contents = json.loads(countries_contents)

    # order of priority: quarantine, reject, secondary, and accept

    # [first order], quarantine
    # create medical list
    medical_list = []
    # collect country code
    for line in countries_contents.values():
        if line["medical_advisory"] != "":
            medical_list.append(line["code"])
    # check if the traveller comes from the country that has a medical advisory
    for entry in input_contents:
        if entry["from"]["country"] in medical_list:
            return["Quarantine"]

    # [second order],secondary
    # create list for watch list info
    first_list = []
    last_list = []
    passport_list = []
    # collect info in lists
    for line in watchlist_contents.values():
        if line["first_name"] !="":
            first_list.append(line["first_name"])
        if line["last_name"] !="":
            last_list.append(line["last_name"])
        if line["passport"] !="":
            passport_list.append(line["passport"])
    # check traveller info vs watchlist
    for entry in input_contents:




    # check incomplete entry
    for entry in input_contents:
        for value in entry.values():
            if value == "":
                return["Reject"]
        for home in entry["home"].values():
            if home == "":
                return["Reject"]
        for froms in entry["from"].values():
            if froms == "":
                return["Reject"]
    #if
    #    return["Reject"]
    #elif
    #    return["Quarantine"]
    #elif
    #    return["Secondary"]
    #else
    #    return ["Accept"]


def valid_passport_format(passport_number):
    """
    Checks whether a pasport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_format = re.compile('.{5}-.{5}-.{5}-.{5}-.{5}')

    if passport_format.match(passport_number):
        return True
    else:
        return False


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    try:
        datetime.datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False
