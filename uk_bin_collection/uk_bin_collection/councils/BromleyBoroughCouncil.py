#!/usr/bin/env python3

# This script pulls (in one hit) the data from
# Warick District Council Bins Data
from bs4 import BeautifulSoup
import dateutil.parser
from uk_bin_collection.uk_bin_collection.common import *
from uk_bin_collection.uk_bin_collection.get_bin_data import AbstractGetBinDataClass


# import the wonderful Beautiful Soup and the URL grabber
class CouncilClass(AbstractGetBinDataClass):
    """
    Concrete classes have to implement all abstract operations of the
    base class. They can also override some operations with a default
    implementation.
    """

    def parse_data(self, page: str, **kwargs) -> dict:
        # Make a BS4 object
        soup = BeautifulSoup(page.text, features="html.parser")
        soup.prettify()

        bin_data_dict = {"bins": []}

        # Search for the specific bin in the table using BS4
        rows = soup.find("div", class_=("waste__collections")).find_all(
            "h3",
            class_=(
                "waste-service-name",
            ),
        )

        # Loops the Rows
        for row in rows:
            bin_type = row.get_text().strip()
            # Date is on the second cell, second paragraph, wrapped in p
            collectionDate = row.find_all_next(
                    "dd", {"class": "govuk-summary-list__value"}
                )[1].text.strip()
            date = dateutil.parser.parse(collectionDate)
            # Make each Bin element in the JSON
            dict_data = {
                "bin_type": bin_type,
                "collectionDate": date.strftime(date_format),
            }
            # # Add data to the main JSON Wrapper
            bin_data_dict["bins"].append(dict_data)

        return bin_data_dict
