import random
from faker import Faker
import datetime
import csv

# random.seed(42)

'''
ID (number, incremental, unique) <- EI 
name, surname <- EI (string, categorical)

birthday <- QI      (number)       01/01/1930 - 31/12/2023
country <- QI       (categorical)  [list of countries]
Zip code <- QI      (number)       16121 - 16167
gender <- QI        (categorical)  [list of genders]
education <- QI     (categorical)  [list of education]

salary <- SD        (real number)        0 - 1000000
height <- SD        (number)        120 - 200
weight <- SD        (number)        40 - 150
condition <- SD     (categorical)   [list condition]
'''

medial_conditions = ["Flu", "Hepatitis", "Brochitis", "Broken Arm", "AIDS", "Hang Nail"]
genders = ["Male", "Female"]

def generateDataset(n = 6, filename = None):
    generated = []
    for i in range(n):
        entry = {
            "ID": i,
            "Age": random.randint(18, 60),
            "Sex": random.choice(genders),
            "Zip-code": random.randint(16121, 16167),
            "Disease": random.choice(medial_conditions)
        }
        generated.append(entry)

    if filename is not None:
        with open(filename, 'w') as csvfile:
            fieldnames = [
                "ID",
                "Age",
                "Sex",
                "Zip-code",
                "Disease"
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in generated:
                writer.writerow(row)

    return generated

#voglio genreare i dati originali del paper
#id 0 : 25, Male, 53711, Flu
#id 1: 25, Female, 53712, Hepatitis
#id 2: 26 Male 53711 Brochitis
#id 3: 27 Male 53710 Broken Arm
#id 4: 27 Female 53712 AIDS
#id 5: 28 Male 53711 Hang Nail

def generatePaperdataset (n= 6, filename = None):
    generated=[]
    entry = {
        "ID": 0,"Age": 25,"Sex": "Male","Zip-code": 53711,"Disease": "Flu",
    }
    generated.append(entry)
    entry = {
        "ID": 1, "Age": 25, "Sex": "Female", "Zip-code": 53712, "Disease": "Hepatitis",
    }
    generated.append(entry)
    entry = {
        "ID": 2, "Age": 26, "Sex": "Male", "Zip-code": 53711, "Disease": "Brochitis",
    }
    generated.append(entry)
    entry = {
        "ID": 3, "Age": 27, "Sex": "Male", "Zip-code": 53710, "Disease": "Broken Arm",
    }
    generated.append(entry)
    entry = {
        "ID": 4, "Age": 27, "Sex": "Female", "Zip-code": 53712, "Disease": "AIDS",
    }
    generated.append(entry)
    entry = {
        "ID": 5, "Age": 28, "Sex": "Male", "Zip-code": 53711, "Disease": "Hang Nail",
    }
    generated.append(entry)

    if filename is not None:
        with open(filename, 'w') as csvfile:
            fieldnames = [
                "ID",
                "Age",
                "Sex",
                "Zip-code",
                "Disease"
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in generated:
                writer.writerow(row)


generateDataset(n = 6, filename="datasetmondrian.csv")
generatePaperdataset(n=6, filename="datasetpaper.csv")

