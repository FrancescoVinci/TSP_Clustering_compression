def jaccard_distance(doc1, doc2) -> float:
    intersection = len(doc1.intersection(doc2))
    union = len(doc1.union(doc2))
    return 1 - intersection / union

def find_medoid(cluster, forward_index_set):
    min_distance_sum = float('inf')
    medoid = None
    for candidate in cluster:
        distance_sum = sum(jaccard_distance(forward_index_set[candidate], forward_index_set[other]) for other in cluster)
        if distance_sum < min_distance_sum:
            min_distance_sum = distance_sum
            medoid = candidate
    return medoid

def stream_cluster(forward_index, radius):
    # Convert forward_index to set representation
    #forward_index_set = {doc: set(terms) for doc, terms in forward_index.items()}
    
    clusters = []
    
    for doc, terms in forward_index.items():
        # Try to assign the document to an existing cluster
        assigned = False
        for medoid, cluster in clusters:
            if jaccard_distance(terms, forward_index[medoid]) <= radius:
                cluster.append(doc)
                assigned = True
                break
        
        # If the document does not fit in an existing cluster, create a new cluster
        if not assigned:
            clusters.append((doc, [doc]))
    
    # Update medoids
    '''
    final_clusters = []
    for medoid, cluster_docs in clusters:
        new_medoid = find_medoid(cluster_docs, forward_index_set)
        final_clusters.append((new_medoid, cluster_docs))
    '''
    
    return clusters


def forward_index(inverted_index):
    forward_index = {}
    term_id = 0

    for _, postings in inverted_index.items():
        for doc in postings:
            if doc not in forward_index:
                forward_index[doc] = []
            forward_index[doc].append(term_id)
        term_id += 1
    
    sorted_fi = dict(sorted(forward_index.items(), key=lambda item: len(item[1]), reverse=True))
    return {doc: set(terms) for doc, terms in sorted_fi.items()}


def clustering(forward_index, radius):
    '''Take an forward index and radius.
    Return clusters and the forward index.

    Input:
    inverted_index: {termID: [postings], ...}
    radius: float

    Output:
    clusters: [(medoid, clustered_docs), ...]
    '''
    #f_i = forward_index(inverted_index)
    clusters = stream_cluster(forward_index, radius)

    return clusters
