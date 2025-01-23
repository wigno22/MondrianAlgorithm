import math

from generate import generateDataset, dict2table, is_float
from generate import generatePaperdataset

from mondrian import find_median
from kanon import is_k_anon
from mondrian import mondrianAnon

import csv
import pandas as pd

from qualityMeasurement import privacy_utility_analysis
from statisticalAnalysis import analysis


def main():
    dataset_name = '29-records-prod'

    # GENERAZIONE DATASET
    generateDataset(29, f'{dataset_name}.csv')

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

    analysis(dataset, dataset_anon, QIs, k_max, f'output/{dataset_name}')

    # endregion


if __name__ == "__main__":
    main()
