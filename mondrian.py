from kanon import is_k_anon


# region FUNCTIONS
def chooseDimension(dataset, QIs, choice):
    dim = None
    if choice:
        # Choose the first attribute of the list
        dim = QIs[0]
    else:
        # Choose the QI with the most different values
        distinct_counts = {QI: len(set(record[QI] for record in dataset)) for QI in QIs}
        dim = max(distinct_counts, key=distinct_counts.get)
    return dim


def find_median(dataset, dim):
    # Estrai i valori della colonna `dim`
    values = [row[dim] for row in dataset]

    # Controlla il tipo di dati
    if isinstance(values[0], (int, float)):  # Numerico
        return median(values)
    elif isinstance(values[0], str):  # Categoriale
        return medianIndex(values)
    else:
        raise ValueError(f"Unsupported data type for dimension: {dim}")


def median(sequence):
    sequence = list(sorted(sequence))
    if len(sequence) % 2 == 0:
        return (sequence[len(sequence) // 2 - 1] + sequence[len(sequence) // 2]) / 2.0
    else:
        return sequence[len(sequence) // 2]


def medianIndex(sequence):
    sequence = list(sorted(sequence))
    return len(sequence) // 2


def splitDataset(dataset, dim, splitVal):
    LHS = None
    RHS = None

    if isinstance(dataset[0][dim], (int, float)):
        # Numerical
        LHS = [record for record in dataset if record[dim] <= splitVal]
        RHS = [record for record in dataset if record[dim] > splitVal]

    elif isinstance(dataset[0][dim], str):
        # Categorical
        dataset_sorted = sorted(dataset, key=lambda x: x[dim])

        LHS = dataset_sorted[:splitVal]
        RHS = dataset_sorted[splitVal:]
    else:
        # TODO: manage the error
        print('Tipo dell\'attributo non gestito')

    return LHS, RHS


def generalize(partition, dim):
    values = [record[dim] for record in partition]
    min_val = min(values)
    max_val = max(values)
    for record in partition:
        if min_val == max_val:
            record[dim] = f'{min_val}'
        else:
            record[dim] = f"[{min_val}-{max_val}]"


# endregion


def mondrianAnon(dataset, QIs, k, choose_dimension=True):
    """
    Makes the dataset k-anonymous by generalizing QIs

    :param dataset: è una lista di record
                    Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param QIs: quasi-identifiers
    :param k: k-anonymization
    :param choose_dimension: SCELTA DELL'ATTRIBUTO DA PARTIZIONARE
    :return: dataset k-anonymized
    """

    # Check if dataset in already K anonymous
    # If True, stop
    if is_k_anon(dataset, QIs, k):
        return dataset

    # Check if I have any QI to partition in order to reach k-anonymization
    # If I have not, stop
    if len(QIs) == 0:
        return dataset

    # Choose one elements inside QIs to split my dataset
    dim = chooseDimension(dataset, QIs, choose_dimension)

    # TODO: cosa fa questa parte dello pseudo-codice?
    # fs ← frequency_set(partition, dim)

    # Find the median value for the chosen attribute (dim)
    # splitVal will be the:
    #   - median value      if it is numerical
    #   - index of median   if it is categorical
    splitVal = find_median(dataset, dim)

    # Split dataset in two partition
    # lhs ← {t ∈ partition : t.dim ≤ splitVal} all the elements <= median (index_of_median)
    # rhs ← {t ∈ partition : t.dim > splitVal} all the elements >  median (index_of_median)
    LHS, RHS = splitDataset(dataset, dim, splitVal)

    # Generalization
    generalize(LHS, dim)
    generalize(RHS, dim)

    for other_dim in QIs:
        if other_dim != dim:
            generalize(LHS, other_dim)
            generalize(RHS, other_dim)

    # Remove the used attributes from the available list
    QIsNew = [q for q in QIs if q != dim]

    # return Anonymize(lhs) ∪ Anonymize(rhs)
    return mondrianAnon(LHS, QIsNew, k, choose_dimension) + mondrianAnon(RHS, QIsNew, k, choose_dimension)
