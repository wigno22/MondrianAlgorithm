from generate import generateDataset
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

    with open('datasets/test_metrics.csv', 'r') as f:
        for row in csv.DictReader(f):
            # TODO: gestire meglio
            row['Age'] = int(row['Age'])
            row['Zipcode'] = int(row['Zipcode'])

            dataset.append(row)

    print(pd.DataFrame.from_dict(dataset), '\n')
    # endregion

    # region TEST mondrianAnon()

    dataset = [
        {'ID': 1, 'Age': 25, 'Sex': 'M', 'Zipcode': '12345', 'Disease': 'Flu'},
        {'ID': 2, 'Age': 35, 'Sex': 'F', 'Zipcode': '12346', 'Disease': 'Cold'},
        {'ID': 3, 'Age': 45, 'Sex': 'M', 'Zipcode': '12347', 'Disease': 'Cancer'},
        {'ID': 4, 'Age': 50, 'Sex': 'F', 'Zipcode': '12348', 'Disease': 'Diabetes'},
        {'ID': 5, 'Age': 23, 'Sex': 'M', 'Zipcode': '12349', 'Disease': 'Flu'},
        {'ID': 6, 'Age': 33, 'Sex': 'F', 'Zipcode': '12350', 'Disease': 'Cold'},
        {'ID': 7, 'Age': 43, 'Sex': 'M', 'Zipcode': '12351', 'Disease': 'Cancer'},
        {'ID': 8, 'Age': 53, 'Sex': 'F', 'Zipcode': '12352', 'Disease': 'Diabetes'},
    ]

    QIs = ['Age', 'Sex', 'Zipcode']
    choose_dim = False

    dataset_after2 = mondrianAnon(dataset, QIs, k=1, choose_dimension=choose_dim)
    df = pd.DataFrame.from_dict(dataset_after2).sort_values(by='ID', ascending=True)
    print(df, '\n')
    
    dataset_after3 = mondrianAnon(dataset, QIs, k=3, choose_dimension=choose_dim)
    df = pd.DataFrame.from_dict(dataset_after3).sort_values(by='ID', ascending=True)
    print(df, '\n\n\n')

    print("!!!!!!!!!!!!!UGUALI!!!!!!!!!!!!!!!!!!!!!") if dataset_after2 == dataset_after3 else None
    # endregion

    # region TEST METRICS
    a(dataset, QIs, K=3, choose_dimension=choose_dim, print_metrics=True)
    # endregion


if __name__ == "__main__":
    main()
