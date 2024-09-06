import csv
from collections import defaultdict

class DuplicateChecker:
    def __init__(self, csv_file_1, csv_file_2):
        # Load donations from two CSV files
        self.donations = self.load_donations(csv_file_1) + self.load_donations(csv_file_2)

    def load_donations(self, csv_file):
        donations = []
        # Read donations from CSV file
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                donations.append(row)
        return donations

    def check_duplicates(self):
        # Replace 'donation_id' with the correct column name from your CSVs
        donation_id_field = 'ID'  # Adjust this based on the actual column name in the files
        
        donation_map = defaultdict(list)
        
        for donation in self.donations:
            donation_id = donation.get(donation_id_field)
            if donation_id:
                donation_map[donation_id].append(donation)

        # Gather full donation details for duplicates
        duplicates = [donations for donations in donation_map.values() if len(donations) > 1]
        return duplicates

    def save_duplicates_to_csv(self, duplicates, output_file):
        if not duplicates:
            print("No duplicates found.")
            return

        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)

            # Write header (using keys of the first donation to get all fields)
            header = duplicates[0][0].keys()  # Assuming the CSVs have the same columns
            writer.writerow(header)

            # Write each duplicate entry to a new row
            for duplicate_list in duplicates:
                for duplicate in duplicate_list:
                    writer.writerow(duplicate.values())

if __name__ == "__main__":
    # Specify input CSV files
    csv_file_1 = "export (7).csv"  # Adjust first file name here
    csv_file_2 = "F & E Active Transactions 9-6-2024 12-51-23 PM.csv"  # Adjust second file name here

    # Initialize DuplicateChecker with two CSV files
    duplicate_checker = DuplicateChecker(csv_file_1, csv_file_2)

    # Check for duplicates
    duplicates = duplicate_checker.check_duplicates()

    if duplicates:
        print("Duplicate Donations:")
        for duplicate_list in duplicates:
            for duplicate in duplicate_list:
                print(f"ID: {duplicate.get('ID', 'N/A')}, Name: {duplicate.get('name', 'N/A')}, Amount: {duplicate.get('amount', 'N/A')}")
    else:
        print("No duplicates found.")

    # Save duplicates to CSV
    duplicate_checker.save_duplicates_to_csv(duplicates, "duplicates_output.csv")
    print("Duplicates saved to 'duplicates_output.csv'")

