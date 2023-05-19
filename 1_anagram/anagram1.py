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

def find_first_idx(target,sorted_list):
    def is_less_than(val):
        return val<target
    return binsearch(sorted_list,is_less_than)

def find_last_idx(target,sorted_list):
    def is_eq_or_less_than(val):
        return val<=target
    return binsearch(sorted_list,is_eq_or_less_than)


def anagram1(target,sorted_seeds,sorted_anagrams):
    target_seed = sorted(target)
    first_idx = find_first_idx(target_seed,sorted_seeds)
    last_idx = find_last_idx(target_seed,sorted_seeds)
    return sorted_anagrams[first_idx+1:last_idx+1]   

def main():
    with open('words.txt','r') as f:
        raw_words = f.read().split("\n")
    seed_anagram_list = [(sorted(raw_word),raw_word) for raw_word in raw_words]
    sorted_seed_anagram_list = sorted(seed_anagram_list)
    sorted_seeds = [pair[0] for pair in sorted_seed_anagram_list]
    sorted_anagrams = [pair[1] for pair in sorted_seed_anagram_list]    
    
    target = input()
    ans = anagram1(target,sorted_seeds,sorted_anagrams)
    print(ans)
    return ans

if __name__ == "__main__":
    main()