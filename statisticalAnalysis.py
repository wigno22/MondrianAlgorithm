from qualityMeasurement import getEquivalentClasses

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

'''
1) DISTRIBUTION
'''

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def showDistributions(dataset):
    # Converti il dataset (lista di dizionari) in un DataFrame
    df = pd.DataFrame(dataset)

    # Escludi la colonna 'ID'
    df = df.drop(columns=['ID'], errors='ignore')

    # Calcola il numero di colonne
    num_attributes = len(df.columns)

    # Crea una griglia di sottotrame
    cols = 3  # Numero di colonne nella griglia
    rows = (num_attributes + cols - 1) // cols  # Numero di righe necessario

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 5, rows * 4))
    axes = axes.flatten()  # Appiattisci la griglia per un accesso più semplice

    for i, attribute in enumerate(df.columns):
        # Plotta la distribuzione per ciascun attributo
        if pd.api.types.is_numeric_dtype(df[attribute]):
            sns.histplot(df[attribute], bins=10, ax=axes[i])
        else:
            sns.countplot(data=df, x=attribute, ax=axes[i], order=df[attribute].value_counts().index)

        axes[i].set_title(f'{attribute} Distribution')
        axes[i].set_xlabel(attribute)
        axes[i].set_ylabel('Count')
        axes[i].tick_params(axis='x', rotation=45)

    # Rimuovi assi vuoti (se il numero di attributi non riempie la griglia)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()  # Adatta la spaziatura tra i grafici
    plt.show()

    # sns.displot(dataset, x="flipper_length_mm", hue="species")
    # sns.displot(dataset, x="Zipcode", hue="species", multiple="stack")


def showDistributionsTogether(dataset):
    df = pd.DataFrame(dataset)

    # Escludi la colonna 'ID'
    df = df.drop(columns=['ID'], errors='ignore')

    # Usa sns.displot per visualizzare la distribuzione di Zipcode separata per 'Sex'
    sns.displot(df, x='Zipcode', hue='Age', kind='kde', multiple='stack')

    # Mostra il grafico
    plt.show()

'''
2) ATTRIBUTES

3) CARDINALITY

4) TUPLES 
    TODO: use this function getEquivalentClasses()
    
5) STD. DEV.

6) MEAN
'''