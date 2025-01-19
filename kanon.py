def is_k_anon(dataset, attrs, k):
    """
    Function that return true|false if dataset is k-anonymous

    k-anonymous means
        for each set of attrs (QI attributes) exists
        at least k rows in dataset with that set of QIs

    # TODO: commentare
    :param dataset:
    :param attrs:
    :param k:

    :return: True or False
    """

    groups = {}
    for row in dataset:
        key = []
        for attr in attrs:
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
