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

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param watchlist_file: The name of a JSON formatted file that contains
        names and passport numbers on a watchlist
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are: "Accept",
        "Reject", "Secondary", and "Quarantine"
    """

    # open files, convert files to python style
    try:
        with open(input_file) as file_reader:
            file_contents = file_reader.read()
            input_contents = json.loads(file_contents.lower())
    except FileNotFoundError:
        raise FileNotFoundError("file not find")
    try:
        with open(watchlist_file) as file_reader:
            file_contents = file_reader.read()
            watchlist_contents = json.loads(file_contents.lower())
    except FileNotFoundError:
        raise FileNotFoundError("file not find")
    try:
        with open(countries_file) as file_reader:
            file_contents = file_reader.read()
            countries_contents = json.loads(file_contents.lower())
    except FileNotFoundError:
        raise FileNotFoundError("file not find")

    # create result list
    result = []
    # create final decision
    decision = []
    # create medical list
    medical_list = []
    # collect country code
    for line in countries_contents.values():
        if line["medical_advisory"] != "":
            medical_list.append(line["code"])

    # create lists for watch list info
    first_list = []
    last_list = []
    passport_list = []

    # collect info in lists
    for line in watchlist_contents:
        if line["first_name"] !="":
            first_list.append(line["first_name"])
        if line["last_name"] !="":
            last_list.append(line["last_name"])
        if line["passport"] !="":
            passport_list.append(line["passport"])

    # create lists for visit visas
    visit_visa_list = []
    for line in countries_contents.values():
        if line["visitor_visa_required"] == "1":
            visit_visa_list.append(line["code"])

    # create lists for transit visas
    transit_visa_list = []
    for line in countries_contents.values():
        if line["transit_visa_required"] == "1":
            transit_visa_list.append(line["code"])

    for entry in input_contents:
        if entry["from"]["country"] in medical_list:
            result.append("Quarantine")
    # check traveller info vs watchlist
        if entry["passport"] in passport_list or entry["first_name"] in first_list or entry["last_name"] in last_list:
            result.append("Secondary")
    # check incomplete entry
        for value in entry.values():
            if value == "":
                result.append("Reject")
        for home in entry["home"].values():
            if home == "":
                result.append("Reject")
        for location in entry["from"].values():
            if location == "":
                result.append("Reject")
    # Check the returning traveller
        if entry["entry_reason"] == "returning":
            for location in entry["from"].values():
                if location == "kan":
                    result.append("Accept")
    # Check traveller from KAN
        for location in entry["from"].values():
            if location == "kan":
                result.append("Accept")
    # check if visiting
        if entry["entry_reason"] == "visit":
            # if country is on visa requirement list
            if entry["home"]["country"] in visit_visa_list:
                try:
                    # check visa date format
                    if valid_date_format(entry["visa"]["date"]) != True:
                        result.append("Reject")
                    # check for valid visa date
                    if valid_visa_date(entry["visa"]["date"]) != True:
                        result.append("Reject")
                except:
                    result.append("Reject")
    # check if in transit
        if entry["entry_reason"] == "transit":
            if entry["home"]["country"] in transit_visa_list:

                    if valid_date_format(entry["visa"]["date"]) != True:
                        result.append("Reject")
                    # check for valid visa date
                    if valid_visa_date(entry["visa"]["date"]) != True:
                        result.append("Reject")
    # check passport format
        if valid_passport_format(entry["passport"]) != True:
            result.append("Reject")
    # check birth date format
        if valid_date_format(entry["birth_date"]) != True:
            result.append("Reject")
    # order of priority: quarantine, reject, secondary, and accept
        if "Quarantine" in result:
            decision.append("Quarantine")
        elif "Reject" in result:
            decision.append("Reject")
        elif "Secondary" in result:
            decision.append("Secondary")
        elif "Accept" in result:
            decision.append("Accept")
        else:
            decision.append("Accept")
    # return decision
    if len(decision)>0:
        return decision

def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
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

def valid_visa_date(date):
    """
    Checks to ensure the visa has a valid date, ie. issue date is < 2 year from current date.
    :param date: visa date being checked
    :return: True if date is within 2 years, False otherwise
    """
    today = datetime.date.today()
    year, month, day = date.split("-")
    visa_date = datetime.date(int(year), int(month),int(day))

    if abs((today-visa_date).days) < 365*2:
        return True
    else:
        return False
