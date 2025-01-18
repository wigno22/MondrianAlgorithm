from generate import generateDataset
from generate import generatePaperdataset

from mondrian import find_median
from kanon import is_k_anon
from mondrian import mondrianAnon

import csv
import pandas as pd

def main():
    # region GENERAZIONE DATASET
    # generateDataset(6, 'prova.csv')
    # generatePaperdataset(6, 'paper.csv')
    # endregion

    # region IMPORTAZIONE DEL DATASET
    dataset = []

    with open('datasets\paper.csv', 'r') as f:
        for row in csv.DictReader(f):
            row['Age'] = int(row['Age'])
            row['Zipcode'] = int(row['Zipcode'])
            dataset.append(row)

    print(type(dataset))
    print(dataset)
    print(pd.DataFrame.from_dict(dataset))

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
    #dataset_after = mondrianAnon(dataset, QIs=['Age', 'Sex'], k=3)

    dataset_after = mondrianAnon(dataset, QIs=['Zipcode', 'Age'], k=2, choose_dimension=True)

    df = pd.DataFrame.from_dict(dataset_after).sort_values(by='ID', ascending=True)

    print(df)
    # endregion


if __name__ == "__main__":
    main()

'''
1 2 3 4 5 6

LHS = [1,2,3]
RHS = [4,5,6]

1 -> [1,2,3] [1-3]
3 -> [1,2,3]
2
5 -> [4,5,6]
4
6
'''