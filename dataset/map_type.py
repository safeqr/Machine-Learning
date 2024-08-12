import pandas as pd

# Load the CSV files
file1 = pd.read_csv('concatenated_split_files1.csv')  
file2 = pd.read_csv('_select_from_safeqr_url_url_left_join_safeqr_qr_code_qr_on_qr_id_202408101634.csv') 

# Function to strip 'http://' or 'https://' from a URL
def strip_protocol(url):
    if isinstance(url, str):
        return url.replace('https://', '').replace('http://', '')
    return url

# Apply the strip function to both file1 and file2 URLs
file1['url_stripped'] = file1['url'].apply(strip_protocol)
file2['contents_stripped'] = file2['contents'].apply(strip_protocol)

# Create a dictionary from the second file for quick lookup of type and qr_code_id
url_type_qr_dict = dict(zip(file2['contents_stripped'], zip(file2['result_category'], file2['qr_code_id'])))

# Prepare a copy of file2 to modify without affecting the original
file2_copy = file2.copy()

# Fill in the result_category in file2_copy
file2_copy['result_category'] = file2_copy['contents_stripped'].map(lambda x: url_type_qr_dict[x][0] if x in url_type_qr_dict else None)

# Drop the id and stripped columns in file2_copy
file2_copy = file2_copy.drop(columns=['id', 'contents_stripped'])

# Prepare a copy of file1 to modify without affecting the original
file1_copy = file1.copy()

# Fill in the qr_code_id in file1_copy based on the match from file2
file1_copy['qr_code_id'] = file1_copy['url_stripped'].map(lambda x: url_type_qr_dict[x][1] if x in url_type_qr_dict else None)

# Drop the stripped column in file1_copy
file1_copy = file1_copy.drop(columns=['url_stripped'])

# Save the updated copies to new CSV files
file1_copy.to_csv('file1_updated.csv', index=False)
file2_copy.to_csv('db_updated.csv', index=False)