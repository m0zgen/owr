#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Created by Yevgeny Goncharov, https://lab.sys-adm.in

import sys
import re
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# Check arg - file or url
if len(sys.argv) != 2:
    print("Необходимо указать 1 аргумент: файл или URL.")
    sys.exit(1)

# Receive file name or URL
source = sys.argv[1]

# Process line function
def process_line(line):
    # Ignore lines starting with #
    if line.strip().startswith("#"):
        return None

    # Extract domain name and extension from string
    matches = re.findall(r'^\*\.(.*?)\.([^.]*)$', line.strip())
    for domain, extension in matches:
        # Apply regular expression to string
        processed_line = re.sub(r'.*\.{0}\.{1}'.format(domain, extension), r'/(^|^.*\.){0}.({1})/'.format(domain, extension), line.strip())
        # Return processed string
        return processed_line

# Function to process data from file
def process_file(file):
    # Process file lines
    with open(file, 'r') as f:
        with ThreadPoolExecutor() as executor:
            results = executor.map(process_line, f)
            for result in results:
                if result is not None:
                    print(result)

# Function to process data from URL
def process_url(url):
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            # Process lines from URL
            with ThreadPoolExecutor() as executor:
                results = executor.map(process_line, data.split('\n'))
                for result in results:
                    if result is not None:
                        print(result)
    except Exception as e:
        print("Ошибка при загрузке файла:", e)
        sys.exit(1)

# Determine the data source and process it
if source.startswith('http://') or source.startswith('https://'):
    process_url(source)
else:
    process_file(source)
