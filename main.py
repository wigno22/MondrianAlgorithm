from generate import generateDataset
from generate import generatePaperdataset

from mondrian import find_median
from kanon import is_k_anon
from refactored import mondrianAnon

import csv
import pandas as pd


def main():
    # region GENERAZIONE DATASET

    # generateDataset(50, 'prova.csv')
    # generatePaperdataset(6, 'paper.csv')

    # endregion

    # region IMPORTAZIONE DEL DATASET
    dataset = []

    with open('datasets/prova.csv', 'r') as f:
        for row in csv.DictReader(f):
            # TODO: gestire meglio
            row['Age'] = int(row['Age'])
            row['Zipcode'] = int(row['Zipcode'])

            dataset.append(row)

    print(pd.DataFrame.from_dict(dataset), '\n')

    # endregion

    # region TEST find_median()
    '''
    mediana_age = find_median(dataset, 'Age')
    mediana_zipcode = find_median(dataset, 'Zipcode')
    mediana_sex = find_median(dataset, 'Sex')
    mediana_disease = find_median(dataset, 'Disease')

    print(mediana_age)
    print(mediana_zipcode)
    print(mediana_sex)
    print(mediana_disease)
    '''
    # endregion

    # region TEST is_k_anon()
    '''
    print(is_k_anon(dataset, ['Age', 'Sex'], k=1))
    print(is_k_anon(dataset, ['Age', 'Sex'], k=2))
    print(is_k_anon(dataset, ['Age', 'Sex'], k=3))

    print(is_k_anon(dataset, [], k=1))
    print(is_k_anon(dataset, [], k=2))
    print(is_k_anon(dataset, [], k=3))
    '''
    # endregion

    # region TEST mondrianAnon()
    dataset_after = mondrianAnon(dataset, QIs=['Sex'], k=40, choose_dimension=True)

    df = pd.DataFrame.from_dict(dataset_after).sort_values(by='ID', ascending=True)

    print(df)
    # endregion


if __name__ == "__main__":
    main()
