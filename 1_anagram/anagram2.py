import sys
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]

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
    
def generatable(seed,target_seed):
    #return if seed can be generated from target_seed
    for i in range(len(seed)):
        if seed[i]<=target_seed[i]:
            pass
        else:
            return False 
    return True

def calc_score(seed):
    res = 0
    for i in range(len(seed)):
        res += seed[i]*SCORES[i]
    return res
        

def anagram2(target_seed,seeds,anagrams):
    """_summary_

    Args:
        target_seed (list): breakdown
        seeds (list): breakdown of alphabets

    Returns:
        _type_: _description_
    """
    max_score = 0
    ans = None
    
    for i in range(len(seeds)):
        seed = seeds[i]
        if generatable(seed,target_seed):
            score = calc_score(seed)
            if score>max_score:
                max_score = score
                ans = anagrams[i]
    return ans

def main(datafile,answerfile):
    raw_words = readwords('words.txt')
    target_words = readwords(datafile)
    breakdown_template = {}
    for i in range(97, 123):
        breakdown_template[chr(i)] = 0
    
    seed_anagram_list = [(breakdown(raw_word,breakdown_template),raw_word) for raw_word in raw_words]
    seeds = [pair[0] for pair in seed_anagram_list]
    anagrams = [pair[1] for pair in seed_anagram_list]
    
    with open(answerfile,'wt') as f:
        for (i,target) in enumerate(target_words):
            target_seed = breakdown(target,breakdown_template)
            ans = ""
            if len(target) == 0 or target_seed == -1:
                ans = ""
            else:
                ans = anagram2(target_seed,seeds,anagrams)
            f.write(ans+"\n")
            if i%20 == 0:
                print(i)

    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])