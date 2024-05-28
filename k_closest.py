# import heapq

# def levenshtein_distance(s1, s2):
#     if len(s1) < len(s2):
#         return levenshtein_distance(s2, s1)

#     if len(s2) == 0:
#         return len(s1)

#     previous_row = range(len(s2) + 1)
#     for i, c1 in enumerate(s1):
#         current_row = [i + 1]
#         for j, c2 in enumerate(s2):
#             insertions = previous_row[j + 1] + 1
#             deletions = current_row[j] + 1
#             substitutions = previous_row[j] + (c1 != c2)
#             current_row.append(min(insertions, deletions, substitutions))
#         previous_row = current_row

#     return previous_row[-1]

# def find_k_closest_words(words, target, k, max_threshold):
#     max_heap = []
    
#     for word in words:
#         distance = levenshtein_distance(word, target)
#         if distance <= max_threshold:
#             heapq.heappush(max_heap, (-distance, word))
#             if len(max_heap) > k:
#                 heapq.heappop(max_heap)
    
#     return [heapq.heappop(max_heap)[1] for _ in range(len(max_heap))][::-1]
import heapq

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1.lower() != c2.lower())
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def find_close_words(words, target, k, max_threshold):
    max_heap = []
    
    for word in words:
        distance = levenshtein_distance(word, target)
        if distance <= max_threshold:
            heapq.heappush(max_heap, (-distance, word))
            if len(max_heap) > k:
                heapq.heappop(max_heap)
    
    return [heapq.heappop(max_heap)[1] for _ in range(len(max_heap))][::-1]

# Example usage
words = ["Dale","Kalle","Bale"]
target = "Damnn my boy"  # Case-sensitive misspelled target
k = 1
max_threshold = 2
print(find_close_words(words,target,k,max_threshold))
# import heapq

# def normalized_levenshtein_distance(s1, s2):
#     if len(s1) < len(s2):
#         return normalized_levenshtein_distance(s2, s1)

#     if len(s2) == 0:
#         return len(s1)

#     previous_row = range(len(s2) + 1)
#     for i, c1 in enumerate(s1):
#         current_row = [i + 1]
#         for j, c2 in enumerate(s2):
#             insertions = previous_row[j + 1] + 1
#             deletions = current_row[j] + 1
#             substitutions = previous_row[j] + (c1.lower() != c2.lower())
#             current_row.append(min(insertions, deletions, substitutions))
#         previous_row = current_row

#     raw_distance = previous_row[-1]
#     normalized_distance = raw_distance / max(len(s1), len(s2))
#     return normalized_distance

# def find_k_closest_words(words, target, k, max_threshold):
#     max_heap = []
    
#     for word in words:
#         distance = normalized_levenshtein_distance(word, target)
#         if distance <= max_threshold:
#             heapq.heappush(max_heap, (-distance, word))
#             if len(max_heap) > k:
#                 heapq.heappop(max_heap)
    
#     return [heapq.heappop(max_heap)[1] for _ in range(len(max_heap))][::-1]

# # Example usage
# words = ["Sameera", "Apple", "ape", "Peach", "apricot", "apply", "P"]
# target = "Sam"  # Case-sensitive target
# k = 3
# max_threshold = .5  # Adjusted threshold for normalized distance

# print(find_k_closest_words(words, target, k, max_threshold))