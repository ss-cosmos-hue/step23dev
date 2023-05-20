import sys
SCORES = [1, 3, 2, 2, 1, 3, 3, 1, 1, 4, 4, 2, 2, 1, 1, 3, 4, 1, 1, 1, 2, 3, 3, 4, 3, 4]
NUM_ALPHABET = 26
INVALID = -1

class WordInfo():
    def __init__(self,raw_word) -> None:
        self.anagram = raw_word 
        self.composition = self.breakdown(raw_word)
        self.score = self.eval(self.composition)
    
    def breakdown(self, word):
        composition = [0]* NUM_ALPHABET#0,1,2,...,25
        for letter in word:
            idx = letter2idx(letter)
            if (idx!= INVALID):
                composition[idx] += 1
            else:
                return INVALID
        return composition
    
    def eval(self,composition):
        score = 0
        if composition != INVALID:
            for i in range(NUM_ALPHABET):
                score += composition[i]*SCORES[i]
            return score
        return INVALID

def letter2idx(letter):
    if 0 <= ord(letter)-ord('a')  <  NUM_ALPHABET:
        return  ord(letter)-ord('a') 
    else:
        return -1

def readwords(filename):
    with open(filename,'r') as f:
        words = f.read().split("\n")
    return words
    
def generatable(seed,target_seed):
    #return if seed can be generated from target_seed
    for i in range(len(seed)):
        if seed[i]<=target_seed[i]:
            pass
        else:
            return False 
    return True
        
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
        if generatable(wordinfo.composition,target_seed):
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
            target_seed = WordInfo(target).composition
            ans = ""
            if len(target) == 0 or target_seed == -1:
                ans = ""
            else:
                ans = anagram2(target_seed,descending_wordinfo_list)
            f.write(ans+"\n")
            if i%50 == 0:
                print(i)

    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])