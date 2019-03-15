import os
import requests
from csv import DictWriter
from bs4 import BeautifulSoup

OUTFILE = "marriage_certs.csv"
URL = "http://search-collections.royalbcmuseum.bc.ca/Genealogy/Results"

FIELDS = [
    "Event Type",
    "Registration Number",
    "Event Date (YYYY-MM-DD)",
    "Event Place",
    "Groom",
    "Bride"
]


def get_genaeology_page(page_num):
    params = {
        "as.type_marriage": True,
        "pageSize": 1000,
        "search": "Search",
        "page": page_num
    }

    return requests.get(URL, data=params).text


def write_csv_row(obj):
    if not os.path.exists(OUTFILE):
        with open(OUTFILE, "w") as csvfile:
            writer = DictWriter(csvfile, FIELDS)
            writer.writeheader()

    with open(OUTFILE, "a") as csvfile:
        writer = DictWriter(csvfile, FIELDS, extrasaction="ignore")
        writer.writerow(obj)


if __name__ == "__main__":

    page_num = 1
    while True:
        print("Page %d" % page_num)

        soup = BeautifulSoup(get_genaeology_page(page_num), "html.parser")
        results = soup.find_all("div", {"class": "fresultsinfo"})

        # If we can't find any more results, we've probably hit the end
        if len(results) == 0:
            break

        for result_item in results:
            result_obj = {}

            rows = result_item.findAll("div", {"class": "fresultsrow"})
            for row in rows:
                result_left = row.find("div", {"class": "fresultsleft"}).text
                result_right = row.find("div", {"class": "fresultsright"}).text

                result_obj[result_left.strip(":")] = result_right

            print(result_obj)
            write_csv_row(result_obj)

        page_num += 1
