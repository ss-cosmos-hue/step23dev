import sys
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
HASHES = [2, 3, 5, 7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101]
NUM_ALPHABET = 26
INVALID = -1

class WordInfo():
    def __init__(self,raw_word) -> None:
        self.anagram = raw_word 
        self.score,self.hash = self.calc_hash_score(raw_word)    

    def calc_hash_score(self, word):
        score = 0
        hash = 1
        for letter in word:
            idx = letter2idx(letter)
            if (idx!= INVALID):
                hash *= HASHES[idx]
                score +=  SCORES[idx] 
            else:
                score, hash = INVALID,INVALID
        return score,hash

def letter2idx(letter):
    if 0 <= ord(letter)-ord('a')  <  NUM_ALPHABET:
        return  ord(letter)-ord('a') 
    else:
        return -1

def readwords(filename):
    with open(filename,'r') as f:
        words = f.read().split("\n")
    return words
    
def generatable(hash,target_hash):
    #return if seed can be generated from target
    return (hash != INVALID) and  (target_hash != INVALID) and  (target_hash % hash == 0)

def anagram2(target_seed,descending_wordinfo_list):
    """_summary_

    Args:
        target_seed (list): breakdown
        seeds (list): breakdown of alphabets

    Returns:
        _type_: _description_
    """

    ans = None
    
    for wordinfo in descending_wordinfo_list:
        if generatable(wordinfo.hash,target_seed):
            ans = wordinfo.anagram
            break
    return ans

def main(datafile,answerfile):
    raw_words = readwords('words.txt')
    target_words = readwords(datafile)   
    wordinfo_list = [WordInfo(raw_word) for raw_word in raw_words]
    descending_wordinfo_list = sorted(wordinfo_list, key = lambda wordinfo: wordinfo.score, reverse=True)

    with open(answerfile,'wt') as f:
        for (i,target) in enumerate(target_words):
            target_hash = WordInfo(target).hash
            ans = ""
            if len(target) == 0 or target_hash == INVALID:
                ans = ""
            else:
                ans = anagram2(target_hash,descending_wordinfo_list)
            f.write(ans+"\n")
            if i%50 == 0:
                print(i)
    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])