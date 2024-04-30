#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Yevgeny Goncharov, https://lab.sys-adm.in

import sys
import re
import urllib.request
import os
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Function to write to a log file
def log_update(output_file):
    log_message = f"File '{output_file}' updated in {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    with open("update_log.txt", "a") as log_file:
        log_file.write(log_message)

# Function to process a line
def process_line(line):
    # Skip lines starting with #
    if line.strip().startswith("#"):
        return None

    # Extract the domain name and extension from the line
    matches = re.findall(r'^\*\.(.*?)\.([^.]*)$', line.strip())
    for domain, extension in matches:
        # Apply a regular expression to the line
        processed_line = re.sub(r'.*\.{0}\.{1}'.format(domain, extension), r'/(^|^.*\.){0}.({1})/'.format(domain, extension), line.strip())
        # Return the processed line
        return processed_line

# Function to download data from URL
def download_data(url):
    try:
        # Check if the etag_cache file exists
        if os.path.exists("etag_cache"):
            with open("etag_cache", "r") as f:
                etag = f.read().strip()
                headers = {"If-None-Match": etag}
                request = urllib.request.Request(url, headers=headers)
        else:
            request = urllib.request.Request(url)

        with urllib.request.urlopen(request) as response:
            # Check the response status code
            if response.status == 200:
                data = response.read().decode('utf-8')
                # Save the new ETag to the cache
                etag = response.getheader("ETag")
                with open("etag_cache", "w") as f:
                    f.write(etag)
                    # Record information in the log
                    log_update(output_file)
                    print("Data is updated.")
                return data
            elif response.status == 304:
                # Source not changed, no need to update data
                print("Source not changed. No need to update data.")
                sys.exit(0)
            else:
                print("Data not loaded. Status code:", response.status)
                sys.exit(1)
    except Exception as e:
        print("Error loading data:", e)
        sys.exit(1)

# Function to process data
def process_data(data):
    processed_data = []
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_line, data.split('\n'))
        for result in results:
            if result is not None:
                processed_data.append(result)
    return "\n".join(processed_data)

# Change to the script directory
script_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(script_dir)

# Determine the data source and process it
if len(sys.argv) < 2 or len(sys.argv) > 3:
    print("Usage: script.py <input_file|URL> [<output_file>]")
    sys.exit(1)

source = sys.argv[1]
output_file = sys.argv[2] if len(sys.argv) == 3 else None

if source.startswith('http://') or source.startswith('https://'):
    data = download_data(source)
else:
    with open(source, 'r') as f:
        data = f.read()

processed_data = process_data(data)

# Output processed data or write to output file
if output_file:
    with open(output_file, 'w') as f:
        f.write(processed_data)
else:
    print(processed_data)
