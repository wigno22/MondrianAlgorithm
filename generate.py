import os

import random
import csv

from faker import Faker
import datetime

medial_conditions = ["Flu", "Hepatitis", "Brochitis", "Broken Arm", "AIDS", "Hang Nail"]
genders = ["Male", "Female"]


def generateDataset(n, filename=None):
    # Crea la cartella datasets se non esiste
    if filename is not None:
        os.makedirs('datasets', exist_ok=True)  # Crea la cartella 'datasets' se non esiste

    generated = []
    for i in range(n):
        entry = {
            "ID": i,
            "Age": random.randint(18, 60),
            "Sex": random.choice(genders),
            "Zipcode": random.randint(16121, 16167),
            "Disease": random.choice(medial_conditions)
        }
        generated.append(entry)

    if filename is not None:
        file_path = os.path.join('datasets', filename)  # Percorso completo del file nella cartella 'datasets'
        with open(file_path, 'w') as csvfile:
            fieldnames = [
                "ID",
                "Age",
                "Sex",
                "Zipcode",
                "Disease"
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in generated:
                writer.writerow(row)

    return generated


def generatePaperdataset(n=6, filename=None):
    # Crea la cartella datasets se non esiste
    if filename is not None:
        os.makedirs('datasets', exist_ok=True)  # Crea la cartella 'datasets' se non esiste

    generated = []
    entry = {
        "ID": 0, "Age": 25, "Sex": "Male", "Zipcode": 53711, "Disease": "Flu",
    }
    generated.append(entry)
    entry = {
        "ID": 1, "Age": 25, "Sex": "Female", "Zipcode": 53712, "Disease": "Hepatitis",
    }
    generated.append(entry)
    entry = {
        "ID": 2, "Age": 26, "Sex": "Male", "Zipcode": 53711, "Disease": "Brochitis",
    }
    generated.append(entry)
    entry = {
        "ID": 3, "Age": 27, "Sex": "Male", "Zipcode": 53710, "Disease": "Broken Arm",
    }
    generated.append(entry)
    entry = {
        "ID": 4, "Age": 27, "Sex": "Female", "Zipcode": 53712, "Disease": "AIDS",
    }
    generated.append(entry)
    entry = {
        "ID": 5, "Age": 28, "Sex": "Male", "Zipcode": 53711, "Disease": "Hang Nail",
    }
    generated.append(entry)

    if filename is not None:
        file_path = os.path.join('datasets', filename)  # Percorso completo del file nella cartella 'datasets'
        with open(file_path, 'w') as csvfile:
            fieldnames = [
                "ID",
                "Age",
                "Sex",
                "Zipcode",
                "Disease"
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in generated:
                writer.writerow(row)

# Esegui il codice di esempio per generare i file
# generateDataset(n = 6, filename="datasetmondrian.csv")
# generatePaperdataset(n=6, filename="datasetpaper.csv")
