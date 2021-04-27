import pickle, json

with open ('n_gram_counts_list.txt', 'rb') as fp:
    n_gram_counts_list = pickle.load(fp)

with open('vocabulary.txt', 'r') as f:
    vocabulary = json.loads(f.read())






def estimate_probability(word, previous_n_gram, 
                         n_gram_counts, n_plus1_gram_counts, vocabulary_size, k=1.0):

    previous_n_gram = tuple(previous_n_gram)
    previous_n_gram_count = n_gram_counts.get(previous_n_gram, 0)
    denominator = previous_n_gram_count + k * vocabulary_size
    n_plus1_gram = (previous_n_gram) + (word,)
    n_plus1_gram_count = n_plus1_gram_counts.get(n_plus1_gram, 0)
    numerator = n_plus1_gram_count + k
    probability = numerator/denominator
    
    return probability




def estimate_probabilities(previous_n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary, k=1.0):
    previous_n_gram = tuple(previous_n_gram)
    vocabulary = vocabulary + ["<e>", "<unk>"]
    vocabulary_size = len(vocabulary)
    probabilities = {}
    for word in vocabulary:
        probability = estimate_probability(word, previous_n_gram, 
                                           n_gram_counts, n_plus1_gram_counts, 
                                           vocabulary_size, k=k)
        probabilities[word] = probability

    return probabilities




def suggest_a_word(previous_tokens, n_gram_counts, n_plus1_gram_counts, vocabulary, k=1.0, start_with=None):

    n = len(list(n_gram_counts.keys())[0]) 
    previous_n_gram = previous_tokens[-n:]
    probabilities = estimate_probabilities(previous_n_gram,
                                           n_gram_counts, n_plus1_gram_counts,
                                           vocabulary, k=k)
    suggestion = None
    max_prob = 0
    for word, prob in probabilities.items():
        if start_with:
            if not word.startswith(start_with):
                continue
        if prob > max_prob:
            suggestion = word
            max_prob = prob
    
    return suggestion, max_prob




def get_suggestions(token, k=1.0, start_with=None):
    previous_tokens = token.lower().split( ' ')
    model_counts = len(n_gram_counts_list)
    suggestions = []
    suggestion_dict = {}
    for i in range(model_counts-1):
        n_gram_counts = n_gram_counts_list[i]
        n_plus1_gram_counts = n_gram_counts_list[i+1]
        
        suggestion = suggest_a_word(previous_tokens, n_gram_counts,
                                    n_plus1_gram_counts, vocabulary,
                                    k=k, start_with=start_with)
        suggestions.append(suggestion)
    
    for item in suggestions:
            suggestion_dict[item[0]] = item[1]

    final_dict = {k: v for k, v in sorted(suggestion_dict.items(), key=lambda item: item[1], reverse=True)}
    dict_keys = [i for i in final_dict.keys()]
    for x in dict_keys:
        if x == '<e>' or dict_keys.count(x) > 1:
            del final_dict[x]
            
    return final_dict