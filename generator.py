from flask import Flask, request, send_from_directory, redirect, url_for, flash
import os
import yaml
import csv
import random
from datetime import datetime, timedelta
from faker import Faker
from werkzeug.utils import secure_filename


def generate_random_data(data_type):
    if data_type == "int":
        return random.randint(1, 1000)
    elif data_type == "string":
        return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', k=10))
    elif data_type == "date":
        start_date = datetime(2000, 1, 1)
        end_date = datetime(2023, 1, 1)
        random_date = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds())))
        return random_date.strftime('%Y-%m-%d')
    elif data_type == "float":
        return round(random.uniform(1, 1000), 2)
    else:
        return None

def generate_csv_from_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        data = yaml.safe_load(file)

    for csv_info in data['csvs']:
        output_path = os.path.join("/app/output", csv_info['name'])
        with open(output_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            headers = [col['name'] for col in csv_info['columns']]
            writer.writerow(headers)
            
            for _ in range(csv_info['rows']):
                row = [generate_random_data(col['type']) for col in csv_info['columns']]
                writer.writerow(row)

if __name__ == "__main__":
    generate_csv_from_yaml('structure.yaml')