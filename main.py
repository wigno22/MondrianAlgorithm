from generate import generateDataset, dict2table
from generate import generatePaperdataset

from mondrian import find_median
from kanon import is_k_anon
from mondrian import mondrianAnon

import csv
import pandas as pd

from test_metrics import a


def main():
    # region GENERAZIONE DATASET
    # generateDataset(1000, 'test_metrics.csv')
    # generatePaperdataset(6, 'paper.csv')
    # endregion

    # region IMPORTAZIONE DEL DATASET
    dataset = []

    with open('datasets/paper.csv', 'r') as f:
        for row in csv.DictReader(f):
            # TODO: gestire meglio
            row['Age'] = int(row['Age'])
            row['Zipcode'] = int(row['Zipcode'])

            dataset.append(row)

    print(pd.DataFrame.from_dict(dataset), '\n')
    # endregion

    # region TEST mondrianAnon()

    QIs = ['Age', 'Zipcode']
    choose_dim = False

    print('k = 2 -------------------------------')
    dataset_after2 = mondrianAnon(dataset, QIs, k=2, choose_dimension=choose_dim)
    print(dict2table(dataset_after2))
    print(f'is 2-anon? {is_k_anon(dataset_after2, QIs, k=2)}')
    print(f'is 3-anon? {is_k_anon(dataset_after2, QIs, k=3)}')
    print(f'is 4-anon? {is_k_anon(dataset_after2, QIs, k=4)}')
    print(f'is 5-anon? {is_k_anon(dataset_after2, QIs, k=5)}')

    '''
    print('k = 5 -------------------------------')
    dataset_after3 = mondrianAnon(dataset, QIs, k=5, choose_dimension=choose_dim)
    print(dict2table(dataset_after3))
    print(f'is 2-anon? {is_k_anon(dataset_after3, QIs, k=2)}')
    print(f'is 3-anon? {is_k_anon(dataset_after3, QIs, k=3)}')
    print(f'is 4-anon? {is_k_anon(dataset_after3, QIs, k=4)}')
    print(f'is 5-anon? {is_k_anon(dataset_after3, QIs, k=5)}')
    '''
    # endregion

    # region TEST METRICS
    # a(dataset, QIs, K=6, choose_dimension=choose_dim, print_metrics=True)
    # endregion


if __name__ == "__main__":
    main()
