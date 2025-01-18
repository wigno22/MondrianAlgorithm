from generate import generateDataset
from generate import generatePaperdataset

from mondrian import find_median

import csv


def main():
    # region GENERAZIONE DATASET
    generateDataset(6, 'prova.csv')
    generatePaperdataset(6, 'paper.csv')
    # endregion

    # region IMPORTAZIONE DEL DATASET
    dataset = []

    with open("pazienti.csv", "r") as f:
        for row in csv.DictReader(f):
            dataset.append(row)

    print(dataset)
    # endregion

    # region TEST find_median()
    mediana_age = find_median(dataset, 'Age')
    mediana_zipcode = find_median(dataset, 'Zipcode')
    mediana_sex = find_median(dataset, 'Sex')
    mediana_disease = find_median(dataset, 'Disease')

    print(mediana_age)
    print(mediana_zipcode)
    print(mediana_sex)
    print(mediana_disease)
    # endregion


if __name__ == "__main__":
    main()
