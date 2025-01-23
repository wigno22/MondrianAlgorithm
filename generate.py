import os

import random
import csv

from faker import Faker
import datetime

import pandas as pd
import numpy as np

random.seed(1)

fake = Faker()

# region ATTRIBUTES
M_names = [
    "Alessandro", "Andrea", "Angelo", "Antonio", "Bruno",
    "Carlo", "Domenico", "Edoardo", "Enrico", "Fabio",
    "Francesco", "Giorgio", "Giovanni", "Giuseppe", "Leonardo",
    "Luca", "Marco", "Matteo", "Michele", "Nicola",
    "Paolo", "Pietro", "Roberto", "Stefano", "Tommaso",
    "Valerio", "Vincenzo", "Raffaele", "Giacomo", "Luciano"
]

F_names = [
    "Maria", "Francesca", "Giulia", "Elena", "Laura",
    "Angela", "Chiara", "Sara", "Paola", "Simona",
    "Alessandra", "Martina", "Valentina", "Lucia", "Giovanna",
    "Anna", "Teresa", "Barbara", "Federica", "Rita",
    "Caterina", "Monica", "Giuseppina", "Silvia", "Isabella",
    "Stefania", "Roberta", "Carla", "Claudia", "Francesca"
]

medial_conditions = ["Flu", "Hepatitis", "Brochitis", "Broken Arm", "AIDS", "Hang Nail"]
genders = ['M', 'F', 'O']
genders_weights = [50, 48, 2]
education = ['None', 'PR', 'MS', 'HS', 'BSc', 'MSc', 'PhD']
education_weights = [2, 8, 10, 30, 25, 20, 5]
# endregion


def generateDataset(n, filename=None):
    # Crea la cartella datasets se non esiste
    if filename is not None:
        os.makedirs('datasets', exist_ok=True)  # Crea la cartella 'datasets' se non esiste

    education_random = random.choices(education, education_weights, k=n)
    genders_random = random.choices(genders, genders_weights, k=n)

    mean_salary = 35000
    std_dev_salary = 10000

    generated = []
    for i in range(n):
        # Salary
        salary = int(np.random.normal(mean_salary, std_dev_salary))
        salary = max(0, salary)

        # Sex
        sex = genders_random[i]
        if sex == 'M':
            name = random.choice(M_names)
        elif sex == 'F':
            name = random.choice(F_names)
        else:
            if random.getrandbits(1):
                name = random.choice(M_names)
            else:
                name = random.choice(F_names)

        entry = {
            "ID": i,
            "Name": name,
            "Age": random.randint(18, 60),
            "Sex": sex,
            "Zipcode": random.randint(16121, 16167),
            "Country": fake.country_code(),
            "Education": education_random[i],
            "Disease": random.choice(medial_conditions),
            "Salary": salary
        }
        generated.append(entry)

    if filename is not None:
        file_path = os.path.join('datasets', filename)  # Percorso completo del file nella cartella 'datasets'
        with open(file_path, 'w') as csvfile:
            fieldnames = [
                "ID",
                "Name",
                "Age",
                "Sex",
                "Zipcode",
                "Country",
                "Education",
                "Disease",
                "Salary"
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


def dict2table(dataset):
    return pd.DataFrame.from_dict(dataset).sort_values(by='ID', ascending=True)


def is_float(value):
    """
    Verifica se un valore può essere convertito in un float.
    """
    try:
        float(value)
        return True
    except ValueError:
        return False


# Esegui il codice di esempio per generare i file
# generateDataset(n = 6, filename="datasetmondrian.csv")
# generatePaperdataset(n=6, filename="datasetpaper.csv")
