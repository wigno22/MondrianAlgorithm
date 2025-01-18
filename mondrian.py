import kanon
from kanon import is_k_anon


def find_median(dataset, dim):
    # Estrai i valori della colonna `dim`
    values = [row[dim] for row in dataset]

    # Controlla il tipo di dati
    if isinstance(values[0], (int, float)):  # Numerico
        return median(values)
    elif isinstance(values[0], str):  # Categoriale
        return median2(values)
    else:
        raise ValueError(f"Unsupported data type for dimension: {dim}")


def median(sequence):
    sequence = list(sorted(sequence))
    median = -1
    if len(sequence) % 2 == 0:
        median = ( sequence[ len(sequence) // 2 -1 ] + sequence[ len(sequence) // 2 ] ) /2
    else:
        median = sequence[ len(sequence) // 2 ]
    return median

def median2(sequence):
    sequence = list(sorted(sequence))
    return sequence[ len(sequence) // 2 ]






# Makes the dataset k-anonymous by
# generalizing QIs
def mondrianAnon(dataset, QIs, k, choose_dimension=True):
    '''
    # TODO: scrivere cosa fa questa funzione

    :param dataset: dataset
    :param QIs: quasi-identifiers
    :param k: k-anonymization
    :param choose_dimension: SCELTA DELL'ATTRIBUTO DA PARTIZIONARE
    :return:
    '''

    # region CHECK K-ANONYMINITY
    # Check if dataset in already K anonymous
    # If true stop
    if is_k_anon(dataset, QIs, k) == True:
        return dataset

    # se non è k anon dovrò generalizzare, splittare il dataset e k anonimizzare
    # endregion

    # region CHECK QI TO GENERALIZE
    # I don't have any new quasi identifiers to generalize
    # in order to reach k-anonymization
    # TODO: verificare che questo controllo funzioni. L'algoritmo passa mai di qui?
    if len(QIs) == 0:
        return dataset
    # else I have some quasi-identifier to generalize
    # endregion

    # region dim ← choose dimension()
    # ^ choose one elements inside QIs to split my dataset
    dim = None
    if choose_dimension:
        # Scelgo il primo attributo della lista
        dim = QIs[0]
    else:
        # choose the QI with the most different values
        values = []
        for QI in QIs:
            # This will create a set with all the distinct values
            # for the currenct quasi-identifier
            values.append( len( set( row[QI] for row in dataset)) )

        # Takes the first element that has the maximum different values
        # inside the dataset
        dim = values[values.index(max(values))]

        '''
        dataset = {
            ZIP CODE = [3, 3, 4, 5, 5, 5, 6, 7, 7, 7, 9] <- set(3, 4, 5, 6, 7, 9) <- 6
            CITY     = [A, A, A, A, B, B, B, B, B, E, E] <- set(A, B, E)          <- 3
            DEGREE   = [B, B, B, B, P, P, P, M, M, H, H] <- set(B, P, M, H)       <- 4
        }
        '''
    # endregion


    # fs ← frequency set(partition, dim)
    # splitV al ← ﬁnd median(f s)
    # ^ find the median value for the choosen attribute (dim)
    # se dim è un valore numerico chiamo median altrimenti median2

    medValue = find_median(dataset, dim)

    print(medValue)

    #lhs ← {t ∈ partition : t.dim ≤ splitV all}
    #rhs ← {t ∈ partition : t.dim > splitV all}
    # ^ split dataset in two partition
    # LHS <- all the elements <= median
    # RHS <- all the elements > median
    LHS = [x for x in dataset if x <= medValue]
    RHS = [x for x in dataset if x >  medValue]

    # TODO: Generalize LHS and RHS according to the previous example

    # Remove the used attributes from the available list
    QIsNew = [q for q in QIs if q != dim]

    # return Anonymize(lhs) ∪ Anonymize(rhs)
    return mondrianAnon(LHS, QIsNew, k, choose_dimension) + mondrianAnon(RHS, QIsNew, k, choose_dimension)


'''
mondrian(dataset, [zip code, city, degree], 3)

generalize and split by city

mondrian(LHS, [zip code, degree], 3) + mondrian(RHS, [zip code, degree], 3)

generalize and split by zip code

mondrian(LHS1, [degree], 3) + mondrian(LHS2, [degree], 3) + ...

generalize and split by degree level

mondrian(LHS11, [], 3) + 


'''
        