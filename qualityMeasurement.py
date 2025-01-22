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

# Funzione per calcolare il livello di generalizzazione e soppressione
def calculate_generalization_and_suppression(dataset_original, dataset_anon, QIs):
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


# Funzione per calcolare Information Loss (IL)

def calculate_information_loss(dataset_original, dataset_anon):
    total_loss = 0
    total_values = dataset_original.size

    for column in dataset_original.columns:
        original_values = dataset_original[column]
        anonymized_values = dataset_anon[column]

        column_loss = sum(original_values != anonymized_values) / len(original_values)
        total_loss += column_loss

    return total_loss / len(dataset_original.columns)


# Funzione per calcolare le Data Utility Metrics

def calculate_data_utility_metrics(dataset_original, dataset_anon, QIs):
    discernability_metric, avg_equiv_class_size = metrics(dataset_anon.to_dict('records'), QIs, k=2)

    # Calcolo della similarità fra distribuzioni pre e post-anonimizzazione
    similarity_scores = {}
    for qi in QIs:
        original_dist = dataset_original[qi].value_counts(normalize=True)
        anonymized_dist = dataset_anon[qi].value_counts(normalize=True).reindex(original_dist.index).fillna(0)

        similarity_scores[qi] = 1 - sum(abs(original_dist - anonymized_dist)) / 2

    return discernability_metric, avg_equiv_class_size, similarity_scores

# Funzione per misurare privacy, utility e ulteriori metriche
def privacy_utility_analysis(dataset, dataset_anon, QIs):
    print("Privacy and Utility Analysis")

    # Convertire i dataset in DataFrame se non lo sono già
    dataset_original = pd.DataFrame.from_dict(dataset) if isinstance(dataset, list) else dataset
    dataset_anon = pd.DataFrame.from_dict(dataset_anon) if isinstance(dataset_anon, list) else dataset_anon

    # Calcolo Generalization e Suppression Level
    generalization_level, suppression_percentage = calculate_generalization_and_suppression(dataset_original, dataset_anon, QIs)
    print(f"Generalization Level: {generalization_level:.4f}")
    print(f"Suppression Percentage: {suppression_percentage:.4f}")

    # Calcolo Information Loss
    information_loss = calculate_information_loss(dataset_original, dataset_anon)
    print(f"Information Loss: {information_loss:.4f}")

    # Calcolo Data Utility Metrics
    discernability_metric, avg_equiv_class_size, similarity_scores = calculate_data_utility_metrics(dataset_original, dataset_anon, QIs)
    print(f"Discernability Metric (Cdm): {discernability_metric}")
    print(f"Normalized Average Equivalence Class Size (Cavg): {avg_equiv_class_size:.4f}")
    for qi, score in similarity_scores.items():
        print(f"Similarity Score for {qi}: {score:.4f}")
