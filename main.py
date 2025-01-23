"""
    Mondrian Algorithm.
    K-anonymize a Dataset using Mondrian Algorithm.

    Authors:
        Andrea Cattarinich, Walter Signoretti.
        Unige, Data Protection & Privacy.

    Paper:
       "Mondrian Multidimensional K-Anonymity"
        by Kristen LeFevre David J. DeWitt Raghu Ramakrishnan, University of Wisconsin, Madison
        https://www.researchgate.net/publication/4234803_Mondrian_Multidimensional_K-Anonymity
"""
import math
from generate import generateDataset, dict2table, is_float
from mondrian import mondrianAnon
import csv
from statisticalAnalysis import analysis


def main():
    dataset_name = '100-record-exam'

    # GENERAZIONE DATASET
    generateDataset(100, f'{dataset_name}.csv')

    # region IMPORTAZIONE DEL DATASET
    dataset = []

    with open(f'datasets/{dataset_name}.csv', 'r') as f:
        for row in csv.DictReader(f):
            for key, value in row.items():
                if value.isdigit():
                    row[key] = int(value)
                elif is_float(value):
                    row[key] = float(value)
                else:
                    row[key] = value

            dataset.append(row)

    print(dict2table(dataset), '\n')
    # endregion

    # region PARAMETERS
    QIs = ['Zipcode', 'Sex', 'Age', 'Country', 'Education']
    choose_dim = False
    k = 4
    k_max = math.floor(len(dataset) / 2)
    # endregion

    # region STATISTICAL ANALYSIS
    dataset_anon = mondrianAnon(dataset, QIs, k, choose_dimension=choose_dim)

    print(dict2table(dataset_anon), '\n')

    analysis(dataset, dataset_anon, QIs, k, k_max, f'output/{dataset_name}')

    # endregion


if __name__ == "__main__":
    main()
