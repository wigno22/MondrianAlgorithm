import copy
from kanon import is_k_anon

# region FUNCTIONS (le funzioni ausiliarie rimangono identiche)
def chooseDimension(dataset, QIs, choice):
    """
    Choose one elements inside QIs to split my dataset

    :param dataset: dataset to be partitioned
    :param QIs: a list of quasi-identifiers
    :param choice: a boolean flag that determines the selection method:
                   - If True, the first attribute in the QIs list is chosen.
                   - If False, the attribute with the most distinct values is selected.
    :return: the selected attribute (dimension) to split the dataset.
    """

    if choice:
        dim = QIs[0]
    else:
        distinct_counts = {QI: len(set(record[QI] for record in dataset)) for QI in QIs}
        dim = max(distinct_counts, key=distinct_counts.get)
    return dim


def find_median(dataset, dim):
    """
    Find the median of a specific attribute (dimension) in a dataset.

    :param dataset: dataset to be partitioned
    :param dim: the dimension (attribute) for which the median is to be calculated
    :return: the median value for numerical data or the median index for categorical data
    """

    # Extract the values of the specified dimension
    values = [row[dim] for row in dataset]

    # Check data type
    if isinstance(values[0], (int, float)):  # Numerical
        return median(values)
    elif isinstance(values[0], str):  # Categorical
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
    """
    Splits the dataset into two subsets based on the given dimension (dim) and split value (splitVal).

    :param dataset: dataset to be split
    :param dim: dimension used for splitting
    :param splitVal: the value used to split the dataset
    :return: LHS (left-hand side) and RHS (right-hand side)
    """

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
        print('Tipo dell\'attributo non gestito')

    return LHS, RHS


def generalize(partition, dim):
    """
    Generalize the values of the specified dimension (dim) in the given partition.

    :param partition: the subset of the dataset to be generalized
    :param dim: the dimension to generalize in the partition
    """

    values = [record[dim] for record in partition]
    min_val = min(values)
    max_val = max(values)
    for record in partition:
        if min_val == max_val:
            record[dim] = f'{min_val}'
        else:
            record[dim] = f"[{min_val}-{max_val}]"
# endregion


def mondrianAnon(dataset, QIs, k, choose_dimension=True, single_dimensional=False):
    """
    Makes the dataset k-anonymous by generalizing quasi-identifiers (QIs)


    :param dataset: the dataset to be partitioned
                    Esempio:    [ {'ID': 0, 'Age': 25, ... }, {'ID': 1, 'Age': 25, ... }, ... ]
    :param QIs: a list of quasi-identifiers
    :param k: the value k for k-anonymization
    :param choose_dimension: boolean flag to determine how to choose the attribute to partition.
                            - if True, use the first attribute
                            - if False, use the one with the most distinct values
    :param single_dimensional: boolean flag to determine if the algorithm should return a single-dimensional anonymized dataset or a multi-dimensional one.
    :return: the k-anonymized dataset
    """

    # Check if dataset in already K anonymous
    # If True, stop
    if is_k_anon(dataset, QIs, k):
        return dataset

    # Check if I have any QI to partition in order to reach k-anonymization
    # If I have not, stop
    if len(QIs) == 0:
        return dataset

    # Check if partition(dataset) is at least as big as the k
    if len(dataset) <= (2*k - 1):
        return dataset

    # Choose one elements inside QIs to split my dataset
    dim = chooseDimension(dataset, QIs, choose_dimension)

    # Find the median value for the chosen attribute (dim)
    splitVal = find_median(dataset, dim)

    # Split dataset in two partition
    LHS, RHS = splitDataset(dataset, dim, splitVal)

    # Copia le partizioni prima di generalizzare
    LHS_copy = copy.deepcopy(LHS)
    RHS_copy = copy.deepcopy(RHS)

    # Generalization
    generalize(LHS_copy, dim)
    generalize(RHS_copy, dim)

    for other_dim in QIs:
        if other_dim != dim:
            if len(LHS_copy) <= (2 * k - 1):
                generalize(LHS_copy, other_dim)
            if len(RHS_copy) <= (2 * k - 1):
                generalize(RHS_copy, other_dim)

    # Remove the used attributes from the available list
    QIsNew = [q for q in QIs if q != dim]

    if single_dimensional:
        return LHS_copy + RHS_copy

    # return Anonymize(lhs) ∪ Anonymize(rhs)
    left = mondrianAnon(LHS_copy, QIsNew, k, choose_dimension)
    right = mondrianAnon(RHS_copy, QIsNew, k, choose_dimension)
    return left + right
