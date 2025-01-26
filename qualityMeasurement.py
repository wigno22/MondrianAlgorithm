from mondrian import mondrianAnon

import pandas as pd
import matplotlib.pyplot as plt


def metrics(dataset, QIs, k, print_metrics=False):
    """
    from a dataset and a list of quasi-identifiers, calculate the two metrics: Cdm and Cavg

    :param dataset: the dataset to be partitioned
                    Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param QIs: a list of quasi-identifiers
    :param k: the value k for k-anonymization
    :param print_metrics: is a boolean value
        if True, the metrics are printed in the console
        else nothing is printed.
    :return: return the two metrics: Cdm and Cavg
    """
    print(f'\nk={k} ------------') if print_metrics else None

    # Equivalent classes
    E = getEquivalentClasses(dataset, QIs)
    total_equiv_classes = len(E)

    # Discernability metric
    Cdm = 0
    for key, value in E.items():
        Cdm += len(value) ** 2
    print(f'Cdm: {Cdm}') if print_metrics else None

    # Normalized average equivalence class size metric
    Cavg = (len(dataset) / total_equiv_classes) / k
    print(f'Cavg: {Cavg}') if print_metrics else None

    return Cdm, Cavg


def getEquivalentClasses(dataset, QIs):
    """
    return the equivalent classes of the dataset, grouped by the QIs
    :param dataset: the dataset to be partitioned
                    Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param QIs: a list of quasi-identifiers
    :return: the equivalent classes of the dataset, grouped by the QIs
    """
    df = pd.DataFrame.from_dict(dataset).sort_values(by='ID', ascending=True)
    return df.groupby(QIs).groups


def compareDiscernability(dataset, QIs, K, choose_dimension=True, print_metrics=False):
    """
     Compare the discernability penalty of multi-dimensional and single-dimensional Mondrian anonymization looking for k from 2 to K.

    :param dataset: the dataset to be partitioned
                    Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param QIs: a list of quasi-identifiers
    :param K: the maximum value of k for k-anonymization
    :param choose_dimension: boolean flag to determine how to choose the attribute to partition.
                            - if True, use the first attribute
                            - if False, use the one with the most distinct values
    :param print_metrics: is a boolean value
        if True, the metrics are printed in the console
        else nothing is printed.
    :return: a plot of the discernability penalty for k from 2 to K
    """
    k_label = []
    discernability_penalty_multi_dimensional_cdm = []
    discernability_penalty_multi_dimensional_cavg = []

    discernability_penalty_single_dimensional_cdm = []
    discernability_penalty_single_dimensional_cavg = []

    for k in range(2, K + 1):
        # Mondrian (multi-dimensional)
        dataset_after_multi_dim = mondrianAnon(dataset, QIs, k, choose_dimension)

        Cdm, Cavg = metrics(dataset_after_multi_dim, QIs, k, print_metrics)
        discernability_penalty_multi_dimensional_cdm.append(Cdm)
        discernability_penalty_multi_dimensional_cavg.append(Cavg)

        k_label.append(k)

        # Mondrian (single-dimensional)
        dataset_after_single_dim = mondrianAnon(dataset, QIs, k, choose_dimension, single_dimensional=True)
        Cdm, Cavg = metrics(dataset_after_single_dim, QIs, k, print_metrics)
        discernability_penalty_single_dimensional_cdm.append(Cdm)
        discernability_penalty_single_dimensional_cavg.append(Cavg)

    # region PLOT GRAPHS
    fig, ax = plt.subplots()

    # Personalization
    ax.set_xlabel('k')
    ax.set_ylabel('Discernability Penalty')
    # ax.set_title('a')
    ax.grid(True)

    ax.plot(
        k_label,
        discernability_penalty_multi_dimensional_cdm,
        '--b',
        label='Multidimensional',
        marker='o',
    )

    ax.plot(
        k_label,
        discernability_penalty_single_dimensional_cdm,
        '--g',
        label='Single-dimensional',
        marker='o',
    )

    ax.legend(loc='lower right')
    # plt.show()
    # endregion

    return fig


def calculate_generalization_and_suppression(dataset_original, dataset_anon, QIs):
    """
    calculate the generalization level and suppression percentage
    :param dataset_original: the dataset to be partitioned
                             Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param dataset_anon:the dataset after anonymization
    :param QIs: a list of quasi-identifiers
    :return: a tuple containing the generalization level and the suppression percentage
    """
    generalization_level = 0
    suppression_count = 0

    for qi in QIs:
        original_unique = dataset_original[qi].nunique()
        anonymized_unique = dataset_anon[qi].nunique()

        generalization_level += (original_unique - anonymized_unique) / original_unique

        suppression_count += dataset_anon[qi].isnull().sum()

    generalization_level /= len(QIs)
    suppression_percentage = suppression_count / dataset_anon.shape[0]

    return generalization_level, suppression_percentage


def calculate_information_loss(dataset_original, dataset_anon):
    """
    calculate the information loss afer anonymization
    :param dataset_original: the dataset to be partitioned
                             Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param dataset_anon:the dataset after anonymization
    :return: a percentage value representing the information loss
    """
    total_loss = 0

    for column in dataset_original.columns:
        original_values = dataset_original[column]
        anonymized_values = dataset_anon[column]

        column_loss = sum(original_values != anonymized_values) / len(original_values)
        total_loss += column_loss

    return total_loss / len(dataset_original.columns)


def privacy_utility_analysis(dataset, dataset_anon, QIs, k):
    """
    generate a table containing all the metrics calculated by the algorithm.
    :param k: k value for k-anonymity
    :param dataset: the dataset to be partitioned
                             Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param dataset_anon:the dataset after anonymization
    :param QIs: a list of quasi-identifiers
    :return: a table containing all the metrics calculated by the algorithm.
    """
    # Convertire i dataset in DataFrame se non lo sono già
    dataset_original = pd.DataFrame.from_dict(dataset) if isinstance(dataset, list) else dataset
    dataset_anon = pd.DataFrame.from_dict(dataset_anon) if isinstance(dataset_anon, list) else dataset_anon

    # Calcolo Generalization e Suppression Level
    generalization_level, suppression_percentage = calculate_generalization_and_suppression(
        dataset_original, dataset_anon, QIs
    )

    # Calcolo Information Loss
    information_loss = calculate_information_loss(dataset_original, dataset_anon)

    # Calcolo Data Utility Metrics
    discernability_metric, avg_equiv_class_size = metrics(dataset_anon, QIs, k)

    # Preparazione dei dati per la tabella
    table_data = [
        ["Metric", "Value"],
        ["Generalization Level", f"{generalization_level:.2f}"],
        ["Suppression Percentage", f"{suppression_percentage:.2f}"],
        ["Information Loss", f"{information_loss:.2f}"],
        ["Discernability Metric (Cdm)", f"{discernability_metric}"],
        ["Normalized Avg. Equiv. Class Size (Cavg)", f"{avg_equiv_class_size:.2f}"],
    ]

    return table_data
