import sys
import time
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
BEGIN_ALPHABET = 97
NUM_ALPHABET = 26
ALPHABETS = [chr(i+BEGIN_ALPHABET) for i in range(NUM_ALPHABET)]
#library は使わないほうがよい? default dictなど

def readwords(filename):
    with open(filename,'r') as f:
        words = f.read().split("\n")
    return words

def breakdown(word,breakdown_template):
    breakdown =  breakdown_template.copy()
    for letter in word:
        if letter in breakdown.keys():
            breakdown[letter]+= 1
        else:
            return -1
    return list(breakdown.values())

def find_till_last_idx(target,sorted_list,corresponding_list):
    low = 0
    n = len(sorted_list)
    high = n-1
    while low<=high:
        mid = (low+high)//2
        if sorted_list[mid]<=target and (mid == n-1 or (mid<n-1 and sorted_list[mid+1]>target)):
            return corresponding_list[:mid+1]
        elif sorted_list[mid]>target:
            high = mid-1
        else:#range内に行ったときも
            low = mid+1
    return []

def det_generatable_indices(target_seed,seed_list_dict,idx_list_dict):
    generatable_indices = {}
    for (i,alphabet) in enumerate(ALPHABETS):
        prop_index_set = set(find_till_last_idx(target_seed[i],seed_list_dict[alphabet],idx_list_dict[alphabet]))
        if i == 0:
            generatable_indices=prop_index_set
        else:
            generatable_indices&=prop_index_set#積集合        
    return list(generatable_indices)

def calc_score(seed):
    res = 0
    for i in range(len(seed)):
        res += seed[i]*SCORES[i]
    return res
        

def anagram2(target_seed,seed_list_dict, idx_list_dict,anagrams,seeds):
    """_summary_

    Args:
        target_seed (list): breakdown
        seeds (list): breakdown of alphabets

    Returns:
        _type_: _description_
    """
    max_score = 0
    ans = ""
    generatable_indices = det_generatable_indices(target_seed,seed_list_dict,idx_list_dict)
    for idx in generatable_indices:
        score = calc_score(seeds[idx])
        if score>max_score:
            max_score = score
            ans = anagrams[idx]
    return ans

def main(datafile,answerfile):
    raw_words = readwords('words.txt')
    target_words = readwords(datafile)
    breakdown_template = {}
    for alphabet in ALPHABETS:
        breakdown_template[alphabet] = 0
    
    seeds = [breakdown(raw_word,breakdown_template) for raw_word in raw_words]

    idx_list_dict = {}
    seed_list_dict = {}

    for (i,alphabet) in enumerate(ALPHABETS):
        numchar_idx_list = sorted([(seed[i],idx) for (idx,seed) in enumerate(seeds)  if seed!= -1 ])  
        seed_list_dict[alphabet] = [numchar_idx[0] for numchar_idx in numchar_idx_list]      
        idx_list_dict[alphabet] = [numchar_idx[1] for numchar_idx in numchar_idx_list]
    
    anagrams = raw_words
    #要素の数ごとにならべかえたら速いかも?
    
    start_time = time.time()
    with open(answerfile,'wt+') as f:
        for (i,target) in enumerate(target_words):
            target_seed = breakdown(target,breakdown_template)
            ans = ""
            if len(target) == 0 or target_seed == -1:
                ans = ""
            else:
                ans = anagram2(target_seed,seed_list_dict,idx_list_dict,anagrams,seeds)
            f.write(ans+"\n")
            if i%20 == 0:
                print(i)
    end_time = time.time()
    print(f'time consumption: {end_time-start_time}\n')
    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])# datafilename and answerfilename expected