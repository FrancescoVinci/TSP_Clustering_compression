from clustering import jaccard_distance


def solve_tsp(medoids, forward_index_set):
    start = medoids[0]
    tour = [start]
    medoids_list = medoids[1:]
    
    current = start
    while medoids_list:
        next_medoid = min(medoids_list, key=lambda medoid: jaccard_distance(forward_index_set[current], forward_index_set[medoid]))
        tour.append(next_medoid)
        medoids_list.remove(next_medoid)
        current = next_medoid
    
    return tour

def apply_tsp_to_medoids(forward_index, clusters):
    """Take a forward index and clusters.
    Return a list of medoids sorted using TSP -> [medoid1, medoid2, ...]

    Input:
    forward_index: {docID: [list_of_term], ...}
    clusters: [(medoid, clustered_docs), ...]

    Output:
    tsp_tour: [docID1, docID2, ...]
    """
    medoids = [medoid for medoid, _ in clusters]
    forward_index_set = {doc: set(terms) for doc, terms in forward_index.items()} # set(terms) because there may be duplicates (multiple identical terms in a document)
    tsp_tour = solve_tsp(medoids, forward_index_set)
    return tsp_tour

def assign_doc_ids(tsp_tour, clusters):
    doc_id = 1
    doc_id_map = {}
    
    medoid_to_docs = {medoid: docs for medoid, docs in clusters}
    
    for medoid in tsp_tour:
        docs = medoid_to_docs[medoid]
        for doc in docs:
            doc_id_map[doc] = doc_id
            doc_id += 1
    
    return doc_id_map

def reassign_postings(postings, doc_id_map):
    new_postings = {}
    for term_id, docs in postings.items():
        new_postings[term_id] = [doc_id_map[doc] for doc in docs]
    return new_postings


def sort_postings(new_postings):
    for term_id, docs in new_postings.items():
        new_postings[term_id] = sorted(docs)
    return new_postings