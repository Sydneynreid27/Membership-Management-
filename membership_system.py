"""
Habitat for Humanity Membership Management System
This program manages a membership system for Habitat for Humanity,
    tracking members' names, donation levels, and total donations.
    It allows users to input new donations, view member data,
    analyze donation statistics, and save/load member information from a CSV file.
"""

import csv
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from typing import Dict, List


# ========================== Data Model ==========================
@dataclass
class Member:
    first_name: str
    last_name: str
    donation_level: str = "No Membership"
    total_donations: float = 0.0

    def full_name(self) -> str:
        # Return the member's full name as 'First Last'
        return f"{self.first_name} {self.last_name}"

    def to_dict(self) -> dict:
        # Convert member to a dictionary for CSV serialization
        return asdict(self)


# ========================== Constants ==========================
TIERS = {
    10000: "Gold",
    5000: "Silver",
    1000: "Bronze"
}

MEMBERSHIP_TIERS_TUPLE = ("Bronze", "Silver", "Gold")


# ========================== Core Functions ==========================
def determine_level(amount: float) -> str:
    # Return membership level based on donation amount.
    for threshold in sorted(TIERS.keys(), reverse=True):
        if amount >= threshold:
            return TIERS[threshold]
    return "No Membership"

def update_member_levels(members: List[Member], donation_data: Dict[str, float]) -> bool:
    # Update member levels based on cumulative total donations, and increment total_donations.
    # Return True if at least one member's level changed.
    changed = False
    for member in members:
        name = member.full_name()
        if name in donation_data:
            amount = donation_data[name]
            # Add this donation to the member's cumulative total
            member.total_donations += amount
            # Determine new level based on updated total donations
            new_level = determine_level(member.total_donations)
            if member.donation_level != new_level:
                old_level = member.donation_level
                print(f"Get donation ${amount:,.2f} from {name}, total ${member.total_donations:,.2f}, {old_level} -> {new_level}")
                member.donation_level = new_level
                changed = True
            else:
                print(f"{name} level unchanged ({new_level}), total donations ${member.total_donations:,.2f}")
    return changed

# ========================== File I/O Functions ==========================
def save_members_to_csv(members: List[Member], filename: str = "members.csv") -> None:
    # Save member information to a CSV file.
    filepath = Path(filename)
    fieldnames = ["first_name", "last_name", "donation_level", "total_donations"]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for member in members:
            writer.writerow(member.to_dict())
    print(f"Saved {len(members)} members to {filename}")


def load_members_from_csv(filename: str = "members.csv") -> List[Member]:
    # Load member information from CSV file
    members = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                row['total_donations'] = float(row['total_donations'])
                members.append(Member(**row))
        print(f"Loaded {len(members)} members from {filename}")
    except FileNotFoundError:
        # Return empty list if file not found.
        print(f"Warning: File {filename} does not exist, returning empty list.")
    return members


# ========================== Data Display Functions ==========================
def show_members(members: List[Member]) -> None:
    # Print a formatted table of all members with their details.
    print("\n" + "=" * 50)
    print("Member Data (Name, Level, Total Donations)")
    if not members:
        print("  No member records.")
    else:
        for m in members:
            print(f"  {m.full_name():<25} {m.donation_level:<15} ${m.total_donations:,.2f}")
    print("=" * 50)


def show_donation_analysis(members: List[Member]) -> None:
    # Perform statistical analysis on member total donations using NumPy.
    print("\n" + "=" * 50)
    if not members:
        print("No member records, cannot analyze donations.")
        print("=" * 50)
        return

    # Extract total donations into a NumPy array for analysis
    arr = np.array([m.total_donations for m in members])
    print("Donation Amount Analysis (based on all members' total donations):")
    print(f"  Number of members: {len(members)}")
    print(f"  Total donations: ${np.sum(arr):,.2f}")
    print(f"  Average donation: ${np.mean(arr):.2f}")
    print(f"  Maximum donation: ${np.max(arr):,.2f}")
    print("=" * 50)


# ========================== Menu Action Handlers ==========================
def handle_add_donation(members: List[Member], donation_data: Dict[str, float]) -> None:
    # Interactively add a new donation for an existing or new member.
    name = input("Member full name (e.g. Frank Castle): ").strip()

    # Repeatedly prompt until valid amount is given
    while True:
        try:
            amount = float(input("Donation amount (USD): "))
            if amount < 0:
                print("Amount cannot be negative. Please re-enter.")
                continue
            break
        except ValueError:
            print("Amount must be a number. Please re-enter.")
    
    # Check if member exists; if not, create a new one with default values
    existing = None
    for m in members:
        if m.full_name() == name:
            existing = m
            break
    if not existing:
        parts = name.split(" ", 1)
        first = parts[0]
        last = parts[1] if len(parts) > 1 else ""
        members.append(Member(first, last, "No Membership", 0.0))
        print(f"New member {name} created (Initial level: No Membership)")
    
    # Add the donation amount to the pending donation data for this member
    donation_data[name] = donation_data.get(name, 0) + amount
    print(f"Recorded donation of ${amount:,.2f} from {name}")


def handle_pending_changes(donation_data: Dict[str, float]) -> None:
    # Show all donations that have been entered but not yet applied.
    if not donation_data:
        print("No pending donation records.")
    else:
        print("\nPending Changes (donations to be processed):")
        for name, amount in donation_data.items():
            print(f"  - {name}: ${amount:,.2f}")
        total_pending = sum(donation_data.values())
        print(f"  Total {len(donation_data)} entries, sum ${total_pending:,.2f}")


def handle_apply_save(members: List[Member], donation_data: Dict[str, float]) -> None:
    # Apply all pending donations to member totals, update levels, and save to CSV.
    if not donation_data:
        print("No pending donations to update.")
        return
    
    print("\nApplying level updates")
    update_member_levels(members, donation_data)
    save_members_to_csv(members)
    # Clear all pending donations after successful save
    donation_data.clear()
    print("Level updates completed, saved to members.csv")


def handle_exit(members: List[Member], donation_data: Dict[str, float]) -> None:
    # Before exiting, check if there are pending donations that haven't been applied.
    if donation_data:
        ans = input("There are unprocessed donations. Apply updates before exiting? (y/n): ").strip().lower()
        if ans == "y":
            update_member_levels(members, donation_data)
            donation_data.clear()
    
    # Display total donations across all members
    total_all = sum(m.total_donations for m in members)
    print(f"Exiting. Total donations across all members: ${total_all:,.2f}")
    # Final save to persist any changes made during exit
    save_members_to_csv(members)
    print("Goodbye!")

# ========================== Main Menu Controller ==========================
def main() -> None:
    # Load existing members from CSV file at startup, and initialize empty donation data dict.
    members = load_members_from_csv()
    donation_data = {}

    # Define menu actions mapping for user input
    menu_actions = {
        "1": lambda: handle_add_donation(members, donation_data),
        "2": lambda: show_members(members),
        "3": lambda: show_donation_analysis(members),
        "4": lambda: handle_pending_changes(donation_data),
        "5": lambda: handle_apply_save(members, donation_data),
        "6": lambda: handle_exit(members, donation_data)
    }

    while True:
        print("\n" + "=" * 40)
        print("Membership Management Menu")
        print("1. Add/Update Donation")
        print("2. View Member Data (Name, Level, Total Donations)")
        print("3. View Donation Analysis")
        print("4. View Pending Changes")
        print("5. Apply Changes and Save")
        print("6. Exit")
        choice = input("Select an option (1-6): ").strip()

        if choice in menu_actions:
            if choice == "6":
                handle_exit(members, donation_data)
                break
            else:
                menu_actions[choice]()
        else:
            print("Invalid option, please re-enter.")


if __name__ == "__main__":
    main()