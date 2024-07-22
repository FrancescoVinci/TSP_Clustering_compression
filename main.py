from create_dictionary import spimi_invert
from compression import convert_to_d_gaps, variable_byte_codes, elias_delta_code, elias_gamma_code
from clustering import clustering
from tsp import apply_tsp_to_medoids, assign_doc_ids, reassign_postings, sort_postings
from rich.console import Console
from rich.table import Text
from log import print_table, print_ii_info, print_cluster_info
import time
import matplotlib.pyplot as plt


def parse_dat_file(file_path):
    documents = {}
    current_doc_id = 0
    with open(file_path, 'r') as file:
        for line in file:
            if current_doc_id >= 27000: # block to 36000 for time reason
                break
            if line.startswith('.I'):
                current_doc_id = int(line.split()[1])
                documents[current_doc_id] = []
            elif line.startswith('.W'):
                continue
            else:
                documents[current_doc_id].extend(line.split())
    return documents


def main(file_path, block_size):
    console = Console()

    console.print(Text(f"Parsing '{file_path}' file..."), style="blue")

    documents = parse_dat_file(file_path)

    console.print(Text("Constructing the inverted index (SPIMI algorithm)...\n", style="blue"))

    inverted_index, num_doc, num_term = spimi_invert(documents, block_size)

    print_ii_info(num_term, num_doc)

    d_gaps_index = convert_to_d_gaps(inverted_index)

    # delta, gamma, VB for the average of bytes used to store the d-gaps
    vb_coding = variable_byte_codes(d_gaps_index)
    gamma_coding = elias_gamma_code(d_gaps_index)
    delta_coding = elias_delta_code(d_gaps_index)

    print_table(vb_coding, gamma_coding, delta_coding)

    
    radiuses = [0.94, 0.95, 0.96, 0.97, 0.98, 0.99]
    times = []
    num_clusters = []
    avg_bytes_vb = []
    avg_bytes_gamma = []
    avg_bytes_delta = []

    for radius in radiuses:
        print("---------------------------")

        console.print(Text(f"Clustering... (radius= {radius})\n", style="bold blue"))

        start_time = time.time()
        clusters, forward_index = clustering(inverted_index, radius)

        print_cluster_info(radius, len(clusters))

        console.print(Text("Solving TSP.....\n", style="blue"))

        tsp = apply_tsp_to_medoids(forward_index, clusters)
        map_docID = assign_doc_ids(tsp, clusters)

        console.print(Text("Reassigning docIDs...\n", style="blue"))
    
        new_inverted_index = reassign_postings(inverted_index, map_docID)
        end_time = time.time()
        tot_time = end_time - start_time

        d_gaps_new_index = convert_to_d_gaps(sort_postings(new_inverted_index))

        # delta, gamma, VB for the average of bytes used to store the d-gaps
        vb_coding_new = variable_byte_codes(d_gaps_new_index)
        gamma_coding_new = elias_gamma_code(d_gaps_new_index)
        delta_coding_new = elias_delta_code(d_gaps_new_index)

        print_table(vb_coding_new, gamma_coding_new, delta_coding_new, True)
        times.append(tot_time)
        num_clusters.append(len(clusters))
        avg_bytes_vb.append(vb_coding_new)
        avg_bytes_gamma.append(gamma_coding_new)
        avg_bytes_delta.append(delta_coding_new)
    
    plt.figure(0)
    plt.plot(num_clusters, times, marker='o')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Execution Time (seconds)')
    plt.title('Execution Time vs. Number of Clusters')
    plt.grid(True)
    plt.savefig("./plot/execution_time_clusters.png")

    plt.figure(1)
    plt.plot(num_clusters, avg_bytes_vb, label="Avg. Bytes VB" ,marker='o')
    plt.plot(num_clusters, avg_bytes_gamma, label="Avg. Bytes Gamma" ,marker='o')
    plt.plot(num_clusters, avg_bytes_delta, label="Avg. Bytes Delta" ,marker='o')
    plt.xlabel('Number of Clusters')
    plt.ylabel('Bytes')
    plt.title('Compression rate per number of clusters')
    plt.grid(True)
    plt.legend() 
    plt.savefig("./plot/compression_rate_clusters.png")






if __name__ == "__main__":
    file_path = './collection/lyrl2004_tokens_test_pt0.dat'
    block_size = 100000 # numero ragionevole per hardware moderno (circa 240 blocchi)
    main(file_path, block_size)
    