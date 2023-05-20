class SeedAnagrams():
    def __init__(self,anagram,seed) -> None:
        self.anagrams = [anagram]
        self.seed = seed
        
    def append_newanag(self,new_anagram):
        self.anagrams.append(new_anagram)
        
class SeedAnagram():
    def __init__(self,anagram) -> None:
        self.anagram = anagram  
        self.seed = sorted(anagram)

def binsearch(sorted_arr,check_condition):
    left = -1
    right = len(sorted_arr)
    while right - left >1:
        mid = (left+right)//2
        if check_condition(sorted_arr[mid]):
            left = mid
        else:
            right = mid 
    return left


def anagram1(target,sorted_seed_anagrams_list):
    target_seed = sorted(target)
    def if_has_leq_seed(seed_anagrams):
        return seed_anagrams.seed <= target_seed
    idx = binsearch(sorted_seed_anagrams_list,if_has_leq_seed)
    if sorted_seed_anagrams_list[idx].seed == target_seed:
        return sorted_seed_anagrams_list[idx].anagrams
    else:
        return None

def main():
    with open('words.txt','r') as f:
        raw_words = f.read().split("\n")
    seed_anagram_list = [SeedAnagram(raw_word) for raw_word in raw_words]
    sorted_seed_anagram_list = sorted(seed_anagram_list, key = lambda seed_anagram: seed_anagram.seed)  
    
    sorted_seed_anagrams_list = []
    pre_seed,cur_seed = None, None
    for i in range(len(sorted_seed_anagram_list)):
        cur_seed = sorted_seed_anagram_list[i].seed 
        cur_anagram = sorted_seed_anagram_list[i].anagram 
        if pre_seed != cur_seed:
            sorted_seed_anagrams_list.append(SeedAnagrams(cur_anagram,cur_seed))
        else:
            sorted_seed_anagrams_list[-1].append_newanag(cur_anagram)
        pre_seed = cur_seed
        
    target = input()
    ans = anagram1(target,sorted_seed_anagrams_list)
    print(ans)
    return ans

if __name__ == "__main__":
    main()