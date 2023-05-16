def find_first_idx(target,sorted_list):
    low = 0
    high = len(sorted_list)-1
    while low<=high:
        mid = (low+high)//2
        if sorted_list[mid]==target and(mid == 0 or (mid>0 and sorted_list[mid-1]<target)) :
            return mid
        elif sorted_list[mid]<target:
            low = mid+1
        else:#range内に行ったときも
            high = mid-1
    return -1

def find_last_idx(target,sorted_list):
    low = 0
    n = len(sorted_list)
    high = n-1
    while low<=high:
        mid = (low+high)//2
        if sorted_list[mid]==target and (mid == n-1 or (mid<n-1 and sorted_list[mid+1]>target)):
            return mid
        elif sorted_list[mid]>target:
            high = mid-1
        else:#range内に行ったときも
            low = mid+1
    return -1

def anagram1(target,sorted_seeds,sorted_anagrams):
    target_seed = sorted(target)
    first_idx = find_first_idx(target_seed,sorted_seeds)
    last_idx = find_last_idx(target_seed,sorted_seeds)
    
    if first_idx == -1:
        return 
    else:
        return sorted_anagrams[first_idx:last_idx+1]   

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