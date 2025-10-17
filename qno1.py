from collections import defaultdict
from typing import List

def group_anagrams(words: List[str]) -> List[List[str]]:

    groups: dict[tuple, list[str]] = defaultdict(list)
    for w in words:
        key = tuple(sorted(w))
        groups[key].append(w)
    return list(groups.values())


if __name__ == "__main__":
    print(group_anagrams(["bat", "tab", "tap", "pat", "cat"]))

