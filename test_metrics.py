from mondrian import mondrianAnon

import pandas as pd
import matplotlib.pyplot as plt


def metrics(dataset, QIs, k, print_metrics=False):
    df = pd.DataFrame.from_dict(dataset).sort_values(by='ID', ascending=True)

    # Equivalent classes
    E = df.groupby(QIs).groups
    print(f'equivalent classes: {E}') if print_metrics else None

    # Total equivalent classes
    total_equiv_classes = len(E)
    print(f'total_equiv_classes: {total_equiv_classes}') if print_metrics else None

    # Discernability metric
    Cdm = 0
    for key, value in E.items():
        Cdm += len(value) ** 2
    print(f'Cdm: {Cdm}') if print_metrics else None

    # Normalized average equivalence class size metric
    Cavg = (len(dataset) / total_equiv_classes) / k
    print(f'Cavg: {Cavg}') if print_metrics else None

    return Cdm, Cavg


def a(dataset, QIs, K, choose_dimension=True):
    k_label = []
    discernability_penalty_multimensional_cdm = []
    discernability_penalty_multimensional_cavg = []

    for k in range(2, K + 1):
        # Mondrian (multi-dimensional)
        dataset_after = mondrianAnon(dataset, QIs, k, choose_dimension)

        Cdm, Cavg = metrics(dataset_after, QIs, k, print_metrics=False)
        discernability_penalty_multimensional_cdm.append(Cdm)
        discernability_penalty_multimensional_cavg.append(Cavg)

        k_label.append(k)

        # TODO: Mondrian (single-dimensional)
        # ...

    # region PLOT GRAPHS
    fig, ax = plt.subplots()

    # Personalization
    ax.set_xlabel('k')
    ax.set_ylabel('Discernability Penalty')
    ax.set_title('a')
    ax.grid(True)

    ax.plot(k_label, discernability_penalty_multimensional_cdm,
            marker='o', linestyle='-', color='blue', label='cdm')

    ax.plot(k_label, discernability_penalty_multimensional_cavg,
            marker='o', linestyle='-', color='lightblue', label='cavg')

    plt.show()
    # endregion
