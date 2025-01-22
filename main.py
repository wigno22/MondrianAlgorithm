import math

from generate import generateDataset, dict2table
from generate import generatePaperdataset

from mondrian import find_median
from kanon import is_k_anon
from mondrian import mondrianAnon

import csv
import pandas as pd

from qualityMeasurement import privacy_utility_analysis
from statisticalAnalysis import analysis


def main():
    # region GENERAZIONE DATASET
    # generateDataset(500, '500-records.csv')
    # generatePaperdataset(6, 'paper.csv')
    # endregion

    # region IMPORTAZIONE DEL DATASET
    dataset = []

    dataset_name = 'test_metrics'

    with open(f'datasets/{dataset_name}.csv', 'r') as f:
        for row in csv.DictReader(f):
            # TODO: gestire meglio
            row['Age'] = int(row['Age'])
            row['Zipcode'] = int(row['Zipcode'])

            dataset.append(row)

    print(pd.DataFrame.from_dict(dataset), '\n')
    # endregion

    QIs = ['Zipcode', 'Sex', 'Age']
    choose_dim = False

    # region TEST mondrianAnon()
    '''
    print('k = 3 -------------------------------')
    dataset_after2 = mondrianAnon(dataset, QIs, k=3, choose_dimension=choose_dim)
    print(dict2table(dataset_after2))
    print(f'is 2-anon? {is_k_anon(dataset_after2, QIs, k=2)}')
    print(f'is 3-anon? {is_k_anon(dataset_after2, QIs, k=3)}')
    print(f'is 4-anon? {is_k_anon(dataset_after2, QIs, k=4)}')
    print(f'is 5-anon? {is_k_anon(dataset_after2, QIs, k=5)}')
    '''
    # endregion

    # region TEST METRICS
    # a(dataset, QIs, K=math.floor(len(dataset)/2), choose_dimension=choose_dim, print_metrics=False)
    # endregion

    # region SINGLE-DIMENSIONAL
    # dataset_after = mondrianAnon(dataset, QIs, k=2, choose_dimension=choose_dim, single_dimensional=True)
    # print(dict2table(dataset_after))

    # endregion

    # region STATISTICAL ANALYSIS
    dataset_anon = mondrianAnon(dataset, QIs, k=3, choose_dimension=choose_dim)
    print(dict2table(dataset_anon))

    analysis(dataset, dataset_anon, QIs, math.floor(len(dataset)/2), f'output/{dataset_name}')

    # endregion

    # testo privacy e utilità
    # privacy_utility_analysis(dataset, dataset_anon, QIs)
    

if __name__ == "__main__":
    main()
