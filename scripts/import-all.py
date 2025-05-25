#!/usr/bin/env python3
"""
imports all data into the database based on config/datasources.yml

Usage:
    python -m scripts.import-all
"""
import yaml
from ghg_scripts.import_utils import ingest_datasource  # new helper that runs processing + load

def main():
    # 1) Load our new YAML manifest instead of manifest.txt
    with open('config/datasources.yml', 'r') as f:
        config = yaml.safe_load(f)

    # 2) Iterate through each datasource, in the order listed
    for entry in config['datasources']:
        name = entry['name']
        print(f"→ Ingesting datasource: {name}")
        # 3) This function should handle processing/raw→processed steps and CSV loading
        ingest_datasource(name)

if __name__ == '__main__':
    main()
