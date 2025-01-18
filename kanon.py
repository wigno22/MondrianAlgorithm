import csv


'''
Function that return true / false
is dataset is k-anonymous

k-anonymous means
for each set of attrs (QI attributes) exists 
at least k rows in dataset with that set of QIs
'''
def is_k_anon(dataset, attrs, k):

    groups = {} # dictionary
    '''
    create a dictionary [attrs] -> rows

    for each row in dataset:
        put row in dictionary[row[attrs]]

    result = all(len(group) >= k for group in dictionary)
    '''
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


'''
small_dataset = []

with open("dataset-small.csv", "r") as f:
    for row in csv.DictReader(f):
        small_dataset.append(row)


print(small_dataset)
print("LENGTH OF DATASET", len(small_dataset))

print("IS DATASET 1-ANON", is_k_anon(small_dataset, ["education"], 1))
print("IS DATASET 2-ANON", is_k_anon(small_dataset, ["education"], 2))
print("IS DATASET 3-ANON", is_k_anon(small_dataset, ["education"], 3))
'''