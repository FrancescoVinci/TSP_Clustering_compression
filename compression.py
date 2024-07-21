import math

def compute_d_gaps(postings_list):
    if not postings_list:
        return []
    
    d_gaps = [postings_list[0]]  # The first ID is the same
    for i in range(1, len(postings_list)):
        d_gaps.append(postings_list[i] - postings_list[i - 1])
    
    return d_gaps

def convert_to_d_gaps(inverted_index):
    d_gaps_index = {term: compute_d_gaps(postings) for term, postings in inverted_index.items()}
    return d_gaps_index


def variable_byte_codes(inverted_index):
    avg_values = []
    for _, postings in inverted_index.items():
        values = 0
        for posting in postings:
            values += math.ceil((math.floor(math.log2(posting))+1)/7)
        avg_values.append(values)
    res = sum(avg_values)/len(avg_values)
    return res

def elias_gamma_code(inverted_index):
    avg_values = []
    for _, postings in inverted_index.items():
        values = 0
        for posting in postings:
            values += (2*math.floor(math.log2(posting))+1)
        avg_values.append(math.ceil(values/8))
    res = sum(avg_values)/len(avg_values)
    return res

def elias_delta_code(inverted_index):
    avg_values = []
    for _, postings in inverted_index.items():
        values = 0
        for posting in postings:
            values += ( math.floor(math.log2(posting)) + (2 * math.floor(math.log2(math.floor(math.log2(posting))+1))+1) )
        avg_values.append(math.ceil(values/8))
    res = sum(avg_values)/len(avg_values)
    return res





        

        




