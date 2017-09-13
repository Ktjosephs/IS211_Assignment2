#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignment2."""

import urllib2
import datetime
import logging
import argparse
import csv

def main():

    def downloadData(url):
        "Bring in URL data"""
        url_data = urllib2.urlopen(url)
        return url_data

    def processData(data):
        """process data"""
        csv_file = csv.reader(data)
        persondict = {}
        csv_file.next()

        for row in csv_file:
            try:
                row[2] = datetime.datetime.strptime(row[2], "%d/%m/%Y")
            except ValueError:
                id_num = int(row[0])
                line = int(row[0])+1
                logger = logging.getLogger("assignment2")
                logger.error(" Error processing line #{} for ID #{}.".format
                             (line, id_num))

            persondict[int(row[0])] = (row[1], row[2])
        return persondict

    def displayPerson(id, persondata):
        """Display info."""
        try:
            response = "Person #{idnum} is {name} with a birthday of {date}"
            print response.format(idnum=id, name=persondata[id][0],
                                  date=persondata[id][1])
        except KeyError:
            print "No match found."

    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="The URL to fetch a CSV file.")
    args = parser.parse_args()
    logging.basicConfig(filename="errors.log", level=logging.ERROR)

    if args.url:
        csvdata = downloadData(args.url)
        persondata = processData(csvdata)
        msg = "Enter an ID # or enter 0 or a negative # to exit. "

        while True:
            try:
                user = int(raw_input(msg))
            except ValueError:
                print "Input is invalid. Please try again."
                continue
            if user > 0:
                displayPerson(user, persondata)
            else:
                print "Thank you."
                sys.exit()
    else:
        print "Please use the --url parameter."


if __name__ == "__main__":
    main()
