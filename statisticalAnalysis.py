import os

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.ticker import MaxNLocator

from qualityMeasurement import privacy_utility_analysis, compareDiscernability


def analysis(before, after, QIs, k, K, output):
    """
    generate a PDF file containing statistical analysis results
    :param before: dataset before anonymization
    :param after: dataset after anonymization
    :param QIs: a  list of quasi-identifiers
    :param k: k value for k-anonymity
    :param K: maximum K value for k-anonymity for discernability penalty analysis
    :param output: name of the output file (PDF)
    """
    output = resolve_filename_conflict(f"{output}.pdf")

    with PdfPages(output) as pdf:
        # Genera la pagina per il primo dataset
        generateDistributionPage(before, pdf, title="Before")

        # Genera la pagina per il secondo dataset
        generateDistributionPage(after, pdf, title="After")

        table = privacy_utility_analysis(before, after, QIs, k)

        generateTablePage(table, pdf, title='Privacy and Utility Analysis')

        fig = compareDiscernability(before, QIs, K, choose_dimension=False, print_metrics=False)

        generateDiscernabilityPenaltyPage(fig, pdf, title='Discernability Penalty Analysis')

    print(f"PDF generato con successo: {output}")


def generateDiscernabilityPenaltyPage(fig, pdf, title):

    """
    print discernability penalty analysis results on a new page
    :param fig: figure object
    :param pdf: file object
    :param title: title of the page
    """

    fig.suptitle(title, fontsize=20, fontweight='bold', y=0.98)

    # Salva la pagina nel PDF
    pdf.savefig(fig)
    plt.close(fig)


def generateTablePage(table_data, pdf, title):

    """
    print table on a new page
    :param table_data: data of the table
    :param pdf: file object
    :param title: title of the page
    """

    fig, ax = plt.subplots(figsize=(8, len(table_data) * 0.6))  # Dimensione dinamica in base al numero di righe
    ax.axis('off')  # Rimuove gli assi

    # Aggiunge la tabella
    table = ax.table(
        cellText=table_data,
        colLabels=None,
        loc='center',
        cellLoc='center',
    )

    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.auto_set_column_width(col=list(range(len(table_data[0]))))

    # Titolo della tabella
    plt.title(title, fontsize=16, fontweight='bold', loc='center', pad=20)

    # Salva la pagina nel PDF
    pdf.savefig(fig)
    plt.close(fig)


def generateDistributionPage(dataset, pdf, title):
    """
    create a new page with a histogram for each attribute in the dataset
    :param dataset: dataset to be analyzed
    :param pdf: file object
    :param title: title of the page
    """
    # Converti il dataset in un DataFrame
    df = pd.DataFrame(dataset)

    # Escludi la colonna 'ID'
    df = df.drop(columns=['ID'], errors='ignore')

    # Calcola il numero di colonne
    num_attributes = len(df.columns)

    # Crea una griglia di sottotrame
    cols = 2  # Numero di colonne nella griglia
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

        # Imposta i valori interi sull'asse y
        axes[i].yaxis.set_major_locator(MaxNLocator(integer=True))

    # Rimuovi assi vuoti (se il numero di attributi non riempie la griglia)
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    # Titolo della pagina
    fig.suptitle(title, fontsize=20, fontweight='bold', y=0.98)

    plt.tight_layout()  # Adatta la spaziatura tra i grafici

    # Salva la pagina nel PDF
    pdf.savefig(fig)
    plt.close(fig)


def resolve_filename_conflict(filepath):
    """
    Risolve i conflitti di nome file aggiungendo un indice crescente al nome del file.

    Args:
        filepath (str): Percorso originale del file.

    Returns:
        str: Percorso del file senza conflitti di nome.
    """
    base, ext = os.path.splitext(filepath)
    counter = 1

    while os.path.exists(filepath):
        filepath = f"{base}_{counter}{ext}"
        counter += 1

    return filepath
