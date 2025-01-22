from mondrian import mondrianAnon

import pandas as pd
import matplotlib.pyplot as plt

from kanon import is_k_anon


def metrics(dataset, QIs, k, print_metrics=False):
    # region DEBUG
    # TODO: togliere queste linee di debug
    print(f'\nk={k} ------------') if print_metrics else None
    for i in range(k, 16):
        print(f'is {i}-anon? {is_k_anon(dataset, QIs, i)}') if print_metrics else None
    # endregion

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
    df = pd.DataFrame.from_dict(dataset).sort_values(by='ID', ascending=True)
    return df.groupby(QIs).groups


def a(dataset, QIs, K, choose_dimension=True, print_metrics=False):
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
    ax.set_title('a')
    ax.grid(True)
    
    '''
    ax.plot(k_label, discernability_penalty_multi_dimensional_cdm,
            marker='o', linestyle='-', color='blue', label='cdm')

    ax.plot(k_label, discernability_penalty_single_dimensional_cdm,
            marker='o', linestyle='-', color='green', label='cdm')

    plt.legend(["Multidimensional", "Single-dimensional"], loc="lower right")
    '''
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
    plt.show()
    # endregion
