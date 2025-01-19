def is_k_anon(dataset, QIs, k):
    """
    Function that return true|false if dataset is k-anonymous

    k-anonymous means
        for each set of attrs (QI attributes) exists
        at least k rows in dataset with that set of QIs

    :param dataset: dataset to check for k-anonymity
    :param QIs: a list of quasi-identifier attributes to check for k-anonymity
    :param k: the value k for k-anonymity

    :return: True if the dataset is k-anonymous, False otherwise
    """

    groups = {}
    for row in dataset:
        key = []
        for attr in QIs:
            key.append(str(row[attr]))

        key = "-".join(key)
        if key not in groups:
            groups[key] = []

        groups[key].append(row)

    result = True
    for group in groups:
        if len(groups[group]) < k:
            result = False
            break

    return result
