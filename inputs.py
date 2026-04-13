# Input data to be called from main program
# Attributes will be first name, last name, donation level

# Import needed tools

import csv
from dataclasses import dataclass

# Define Member dataclass

@dataclass
class Member:
    first_name: str
    last_name: str
    donation_level: str

# List members and save to CSV file, members.csv

members = [Member("Frank", "Castle", "Bronze"), Member("Gwen", "Stacy", "Silver"), Member("Cindy", "Moon", "Gold"),]
with open("members.csv", "w", newline="") as f:
    writer = csv.writer(f) # Creates a CSV writer object and links it to open file
    writer.writerow(["first_name", "last_name", "donation_level"]) # Writes header row in members.csv
    for d in members:
        writer.writerow([d.first_name, d.last_name, d.donation_level]) # Writes remainder of CSV rows

# Load CSV file
with open("members.csv", "r") as f:
    reader = csv.DictReader(f)
    members = [Member(**row) for row in reader]