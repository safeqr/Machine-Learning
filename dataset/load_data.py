import csv
import os
import requests
import concurrent.futures

# Define the endpoint URL
endpoint_url = "http://localhost:8080/v1/qrcodetypes/scan"

# Path to the CSV file
csv_file_path = "hasExecutable.csv"

# Directory to store the split CSV files
split_files_dir = "split_csv_files"
os.makedirs(split_files_dir, exist_ok=True)

# File to store failed requests
failed_requests_file = "failed_requests.csv"

# Final concatenated CSV file
final_concatenated_file = "concatenated_split_files.csv"

# Function to ensure URL starts with http:// or https://
def ensure_url_prefix(url):
    if not (url.startswith("http://") or url.startswith("https://")):
        return "https://" + url
    return url

# Read the CSV file and split into 199 files
def split_csv_file(csv_file_path, split_files_dir, num_splits=199):
    with open(csv_file_path, newline='') as csvfile:
        reader = list(csv.DictReader(csvfile))
        total_rows = len(reader)
        rows_per_file = total_rows // num_splits
        
        for i in range(num_splits):
            split_file_path = os.path.join(split_files_dir, f"split_file_{i+1}.csv")
            with open(split_file_path, 'w', newline='') as split_file:
                writer = csv.DictWriter(split_file, fieldnames=['url', 'type'])
                writer.writeheader()
                start_index = i * rows_per_file
                end_index = (i + 1) * rows_per_file if i != num_splits - 1 else total_rows
                for row in reader[start_index:end_index]:
                    row['url'] = ensure_url_prefix(row['url'])
                    writer.writerow(row)

# Function to process a CSV file and send POST requests
def process_csv_file(csv_file_path):
    failed_requests = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            url = row['url']  # Column header for URL is 'url'
            response = requests.post(endpoint_url, json={"data": url})
            if response.status_code == 200:
                print(f"Successfully sent data: {url}")
            else:
                print(f"Failed to send data: {url}, Status code: {response.status_code}")
                failed_requests.append({"url": url, "status_code": response.status_code})
    return failed_requests

# Function to write failed requests to a CSV file
def write_failed_requests(failed_requests):
    if not failed_requests:
        return
    with open(failed_requests_file, 'w', newline='') as csvfile:
        fieldnames = ['url', 'status_code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for request in failed_requests:
            writer.writerow(request)

# Function to concatenate all split CSV files into one
def concatenate_csv_files(split_files_dir, output_file):
    fieldnames = ['url', 'type']
    with open(output_file, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for file in os.listdir(split_files_dir):
            if file.endswith('.csv'):
                with open(os.path.join(split_files_dir, file), newline='') as infile:
                    reader = csv.DictReader(infile)
                    for row in reader:
                        writer.writerow(row)

# Split the original CSV file into 199 parts
split_csv_file(csv_file_path, split_files_dir)

# Get the list of split CSV files
split_files = [os.path.join(split_files_dir, file) for file in os.listdir(split_files_dir) if file.endswith('.csv')]

# Execute the requests concurrently with 199 threads
all_failed_requests = []
with concurrent.futures.ThreadPoolExecutor(max_workers=199) as executor:
    futures = [executor.submit(process_csv_file, split_file) for split_file in split_files]
    for future in concurrent.futures.as_completed(futures):
        all_failed_requests.extend(future.result())

# Write all failed requests to a file
write_failed_requests(all_failed_requests)

# Concatenate all split CSV files into one final file
concatenate_csv_files(split_files_dir, final_concatenated_file)

print("Processing completed.")
