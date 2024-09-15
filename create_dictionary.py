from collections import defaultdict
import os

def spimi_invert(documents, block_size):
    index = defaultdict(list)
    current_block_size = 0
    block_id = 0
    doc_count = 0
    term_count = 0

    for doc_id, terms in documents.items():
        doc_count += 1
        for term in terms:
            if term not in index:
                term_count += 1
                index[term] = []
            index[term].append(doc_id)
            current_block_size += 1
            if current_block_size >= block_size:
                write_block_to_disk(index, block_id)
                index = defaultdict(list)
                current_block_size = 0
                block_id += 1

    if current_block_size > 0:
        write_block_to_disk(index, block_id)

    final_index = merge_blocks(block_id)

    return final_index, doc_count, term_count

def write_block_to_disk(index, block_id):
    file_name = f"block_{block_id}.txt"
    with open("./blocks/" + file_name, 'w') as file:
        for term, postings in index.items():
            unique_postings = sorted(set(postings))  # rimuove duplicati e ordina
            file.write(f"{term}:{' '.join(map(str, unique_postings))}\n")

def merge_blocks(num_blocks):
    final_index = defaultdict(list)
    for block_id in range(num_blocks + 1):
        file_name = f"block_{block_id}.txt"
        with open("./blocks/" + file_name, 'r') as file:
            for line in file:
                term, postings = line.strip().split(':')
                final_index[term].extend(map(int, postings.split()))

    for block_id in range(num_blocks + 1):
        os.remove("./blocks/" + f"block_{block_id}.txt")

    for term in final_index:
        final_index[term] = sorted(set(final_index[term]))

    return final_index