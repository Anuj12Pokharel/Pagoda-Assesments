

#### Problem relies with original code

Memory waste: nums creates a full list of 1,000,000 integers unnecessarily.
Extra work: loop visits every number (odds and evens) and checks n % 2 == 0 for each — extra branching.
Python loop overhead: appending in a loop is slower than a list comprehension implemented in C. 


#### Why this method is better


Uses range(0, n, 2) to iterate only even numbers → half the iterations compared to iterating all numbers.
Uses a list comprehension which is implemented in C and is faster than an explicit Python for + append.
Time complexity: still O(n) in Big-O (more precisely O(n/2)), but with a ~2× reduction in iterations vs original.
Memory: uses memory only for the final squares list (size ≈ n/2). No nums temporary list.