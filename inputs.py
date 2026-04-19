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

# Function to determine membership level based on donation amount
def determine_level(amount):
    if amount >= 10000:
        return "Gold"
    elif amount >= 5000:
        return "Silver"
    elif amount >= 1000:
        return "Bronze"
    else:
        return "No Membership."

# Example: simulate donation amounts for existing members
donation_data = {
    "Frank Castle": 1200,
    "Gwen Stacy": 6000,
    "Cindy Moon": 15000
}

# Apply logic to update membership levels
for m in members:
    full_name = f"{m.first_name} {m.last_name}"
    if full_name in donation_data:
        calculated_level = determine_level(donation_data[full_name])
        print(f"{full_name} donated ${donation_data[full_name]} → {calculated_level}")
# Check if stored membership level matches calculated level
for m in members:
    full_name = f"{m.first_name} {m.last_name}"
    
    if full_name in donation_data:
        actual_amount = donation_data[full_name]
        expected_level = determine_level(actual_amount)
        
        if m.donation_level != expected_level:
            print(f"WARNING: {full_name} is listed as {m.donation_level} but should be {expected_level}")
        else:
            print(f"{full_name} membership is correct ({m.donation_level})")
