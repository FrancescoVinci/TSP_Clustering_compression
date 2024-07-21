from rich.console import Console
from rich.table import Table, Text

console = Console()

def print_table(vb_coding, gamma_coding, delta_coding, tsp_clustering=False):
    encodings_table = Table(title="W/o TSP clustering")
    if tsp_clustering:
        encodings_table = Table(title="With TSP clustering")

    rows = [
        ["VB Coding", f"{round(vb_coding, 4)}"],
        ["Elias Gamma", f"{round(gamma_coding, 4)}"],
        ["Elias Delta", f"{round(delta_coding, 4)}"],
    ]

    encodings_table.add_column("Encoding")
    encodings_table.add_column("Avg. byte", style="bright_green")

    for row in rows:
        encodings_table.add_row(*row)

    console.print(encodings_table)

def print_ii_info(num_term, num_doc):
    u_terms_text = Text("Number of unique term: ", style="bold magenta")
    u_terms_text.append(f"{num_term}", style="bright_green")
    n_docs_text = Text("Number of document: ", style="bold magenta")
    n_docs_text.append(f"{num_doc}\n", style="bright_green")
    console.print(u_terms_text)
    console.print(n_docs_text)

def print_cluster_info(radius, len_clusters):
    clusters_text = Text("Radius: ", style="bold magenta")
    clusters_text.append(f"{radius}", style="bright_green")
    clusters_n_text = Text("Number of clusters: ", style="bold magenta")
    clusters_n_text.append(f"{len_clusters}\n", style="bright_green")
    console.print(clusters_text)
    console.print(clusters_n_text)
