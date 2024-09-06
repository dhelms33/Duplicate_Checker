import csv
from collections import defaultdict

class DuplicateChecker:
    def __init__(self, donations):
        self.donations = donations

    def check_duplicates(self):
        # Using defaultdict to store donations by donation_id
        donation_map = defaultdict(list)
        
        for donation in self.donations:
            donation_id = donation['donation_id']
            donation_map[donation_id].append(donation)

        # Gather full donation details for duplicates (those with more than one entry)
        duplicates = [donations for donations in donation_map.values() if len(donations) > 1]
        return duplicates

    def save_duplicates_to_csv(self, duplicates, output_file):
        # Writing duplicates to a CSV file
        with open(output_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write header
            writer.writerow(["Donation ID", "Name", "Amount"])
            for duplicate_list in duplicates:
                for duplicate in duplicate_list:
                    writer.writerow([duplicate['donation_id'], duplicate['name'], duplicate['amount']])

if __name__ == "__main__":
    from database_fetcher import CureCRMFetcher, ClassyFetcher, DynamicsFetcher, DonationDataManager

    # Initialize fetchers for each system
    fetchers = [CureCRMFetcher(), ClassyFetcher(), DynamicsFetcher()]

    # Create a manager to handle fetching from all systems
    manager = DonationDataManager(fetchers)

    # Fetch all donations
    donations = manager.get_all_donations()

    # Initialize DuplicateChecker with fetched donations
    duplicate_checker = DuplicateChecker(donations)

    # Check for duplicates
    duplicates = duplicate_checker.check_duplicates()

    # Print duplicates
    print("Duplicate Donations:")
    for duplicate_list in duplicates:
        for duplicate in duplicate_list:
            print(f"ID: {duplicate['donation_id']}, Name: {duplicate['name']}, Amount: {duplicate['amount']}")

    # Save duplicates to CSV
    duplicate_checker.save_duplicates_to_csv(duplicates, "duplicates_output.csv")
    print("Duplicates saved to 'duplicates_output.csv'")