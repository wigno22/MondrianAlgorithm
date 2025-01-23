import os

import random
import csv

from faker import Faker

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

european_countries = [
    "AT", "BE", "BG", "HR", "CZ",        # Austria, Belgium, Bulgaria, Croatia, Czech Republic
    "DK", "FI", "FR", "DE", "GR",        # Denmark, Finland, France, Germany, Greece
    "HU", "IS", "IE", "IT",              # Hungary, Iceland, Ireland, Italy,
    "LU", "NL", "NO", "PL", "PT",        # Luxembourg, Netherlands, Norway, Poland, Portugal
    "RO", "SK", "SI", "ES", "SE", "CH",  # Romania, Slovakia, Slovenia, Spain, Sweden, Switzerland
    "GB"                                 # United Kingdom
]

medial_conditions = ["Flu", "Hepatitis", "Brochitis", "Broken Arm", "AIDS", "Hang Nail"]
genders = ['M', 'F', 'O']
genders_weights = [50, 48, 2]
education = ['None', 'PR', 'MS', 'HS', 'BSc', 'MSc', 'PhD']
education_weights = [2, 8, 10, 30, 25, 20, 5]
# endregion


def generateDataset(n, filename=None):
    """
    Generate a synthetic dataset containing information about individuals and optionally save it to a CSV file.

    :param n: int
    Number of records to generate in the dataset.
    :param filename: str, optional
    Name of the CSV file where the dataset will be saved. If None, the dataset will not be saved to a file.
    :return: list
    A list of dictionaries, each representing a record in the dataset.

    If the number of records (n) exceeds 30, male and female names are reduced to a subset of at most 15 names to improve histogram readability.
    The generated dataset can be saved to a CSV file in the 'datasets' directory, which will be automatically created if it does not exist.

    """
    # Crea la cartella datasets se non esiste
    if filename is not None:
        os.makedirs('datasets', exist_ok=True)  # Crea la cartella 'datasets' se non esiste

    #se dataset ha più di 30 records, riduciamo a 15 il dominio dei nomi per rappresentarli meglio
    #altrimenti lascio dominio originale
    if n>30:
        max_names=15
        M_names_reduced= random.sample(M_names, min(len(M_names), max_names))
        F_names_reduced= random.sample(F_names, min(len(F_names), max_names))
    else:
        M_names_reduced=M_names
        F_names_reduced=F_names

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
            name = random.choice(M_names_reduced)
        elif sex == 'F':
            name = random.choice(F_names_reduced)
        else:
            if random.getrandbits(1):
                name = random.choice(M_names_reduced)
            else:
                name = random.choice(F_names_reduced)

        entry = {
            "ID": i,
            "Name": name,
            "Age": random.randint(18, 60),
            "Sex": sex,
            "Zipcode": random.randint(16121, 16167),
            "Country": random.choice(european_countries),
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


def generatePaperdataset(filename=None):

    """
    create the dataset used in the paper("Mondrian Multidimensional K-Anonymity") at page:1
    Kristen LeFevre David J. DeWitt Raghu Ramakrishnan, University of Wisconsin, Madison
    https://www.researchgate.net/publication/4234803_Mondrian_Multidimensional_K-Anonymity
    """

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
    """
    transform a dataset in a pandas dataframe
    """
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


