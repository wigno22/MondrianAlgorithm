from generate import generateDataset
from generate import generatePaperdataset

from mondrian import find_median
from kanon import is_k_anon
from mondrian import mondrianAnon

import csv
import pandas as pd


def main():

    # region GENERAZIONE DATASET
    # generateDataset(50, 'prova.csv')
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
    dataset_after = mondrianAnon(dataset, QIs=['Zipcode','Age','Sex'], k=2, choose_dimension=False)
    df = pd.DataFrame.from_dict(dataset_after).sort_values(by='ID', ascending=True)
    print(df)
    # endregion


if __name__ == "__main__":
    main()
