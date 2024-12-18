import csv
from io import TextIOWrapper

def parse_csv(file):
    """
    Parse a CSV file into a list of dictionaries.
    """
    csv_file = TextIOWrapper(file, encoding="utf-8")
    reader = csv.DictReader(csv_file)
    return [row for row in reader]
