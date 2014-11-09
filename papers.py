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
    # example_entries.json
    try:
        with open(input_file, "r") as input_reader:
            #File to string
            input_contents = input_reader.read()
            #string load to dict/list, each entry in list is 1 record in the json
            input_contents = json.loads(input_contents.lower())
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find file")
    try:
        with open(watchlist_file, "r") as watchlist_reader:
            watchlist_contents = watchlist_reader.read()
            watchlist_contents = json.loads(watchlist_contents.lower())
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find file")
    try:
        with open(countries_file, "r") as countries_reader:
            countries_contents = countries_reader.read()
            countries_contents = json.loads(countries_contents.lower())
    except FileNotFoundError:
        raise FileNotFoundError("Cannot find file")
    # create result list
    result = []
    # order of priority: quarantine, reject, secondary, and accept
    # create medical list
    medical_list = []
    # collect country code
    #dictionary values()
    for line in countries_contents.values():
        if line["medical_advisory"] != "":
            medical_list.append(line["code"])
    # check if the traveller comes from the country that has a medical advisory
    #entry is a genetic/var
    for entry in input_contents:
        if entry["from"]["country"] in medical_list:
            result.append("Quarantine")

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
        if entry["passport"] in passport_list or entry["first_name"] in first_list or entry["last_name"] in last_list:
            result.append("Secondary")

    # check incomplete entry
    for entry in input_contents:
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
    for entry in input_contents:
        if entry["entry_reason"] == "returning":
            for location in entry["from"].values():
                if location == "kan":
                    result.append("Accept")
    for entry in input_contents:
        for location in entry["from"].values():
            if location == "kan":
                result.append("Accept")

    # create lists for visit visas
    visit_visa_list = []
    for line in countries_contents.values():
        if line["visitor_visa_required"] == 1:
            visit_visa_list.append(line["code"])

    # create lists for transit visas
    transit_visa_list = []
    for line in countries_contents.values():
        if line["transit_visa_required"] == 1:
            transit_visa_list.append(line["code"])

    # check if visiting
    for entry in input_contents:
        if entry["entry_reason"] == "visit":
            # if country is on visa requirement list
            if entry["home"]["country"] in visit_visa_list:
                try:
                    # check for valid visa date
                    if valid_visa_date(entry["visa"]["date"]) != True:
                        result.append("Reject")
                except:
                    result.append("Reject")

    # check if in transit
    for entry in input_contents:
        if entry["entry_reason"] == "transit":
            if entry["home"]["country"] in transit_visa_list:
                try:
                    if valid_visa_date(entry["visa"]["date"]) != True:
                        result.append("Reject")
                except:
                    result.append("Reject")

    # final decision
    if "Quarantine" in result:
        return["Quarantine"]
    elif "Reject" in result:
        return["Reject"]
    elif "Secondary" in result:
        return["Secondary"]
    elif "Accept" in result:
        return ["Accept"]
    else:
        return ["Accept"]


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

    valid_by_date = datetime.datetime.now() - datetime.timedelta(days=2*365.25)
    if valid_by_date.strftime("%Y-%m-%d") < date.strftime("%Y-%m-%d"):
        return True
    else:
        return False
