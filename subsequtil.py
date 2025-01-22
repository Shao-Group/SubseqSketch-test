import random

ALPHABET=['A','C','G','T']

'''
Return a random string of the given length from ALPHABET.
'''
def randSeq(length):
    return ''.join(random.choices(ALPHABET, k=length))


def randSingleMutation(s):
    p = random.randrange(len(s))
    result = s[:p]

    mutation_type = random.randrange(3)
    if mutation_type == 0: #insertion
        mutation_char = random.randrange(len(ALPHABET))
        result += ALPHABET[mutation_char]
        result += s[p:]
    elif mutation_type == 1: #deletion
        result += s[p+1:]
    else: #substitution
        mutation_char = random.randrange(len(ALPHABET)-1)
        if mutation_char >= ALPHABET.index(s[p]):
            mutation_char += 1
        result += ALPHABET[mutation_char]
        result += s[p+1:]

    return result
            
'''
For each position of s, apply a mutation with probability rate.
The mutation is chosen uniformly at random from insertion (4 kinds),
deletion, and substitution (3 kinds).
'''
def randMutation(s, rate):
    result = []
    i = 0
    while i < len(s):
        if random.random() < rate:
            # the following treat each possible mutation equally which largely bias towards insertion
            '''
            mutation = random.randrange(len(ALPHABET)<<1)
            if mutation < len(ALPHABET): #insertion
                result.append(ALPHABET[mutation])
                result.append(s[i])
            else:
                mutation -= len(ALPHABET)
                if ALPHABET[mutation] == s[i]: #deletion
                    pass
                else: #substitution
                    result.append(ALPHABET[mutation])
            '''
            mutation_type = random.randrange(3)
            if mutation_type == 0: #insertion
                mutation_char = random.randrange(len(ALPHABET))
                result.append(ALPHABET[mutation_char])
                result.append(s[i])
            elif mutation_type == 1: #deletion
                pass
            else: #substitution
                mutation_char = random.randrange(len(ALPHABET)-1)
                if mutation_char >= ALPHABET.index(s[i]):
                    mutation_char += 1
                result.append(ALPHABET[mutation_char])
        else:
            result.append(s[i])

        i += 1

    return ''.join(result)


'''
Return a random subsequence of s of the given length.
'''
def randSubseq(s, length):
    return ''.join([s[i] for i in sorted(random.sample(range(len(s)), length))])


'''
Test if s is a subsequence of t.
By @falsetru from https://stackoverflow.com/questions/24017363/how-to-test-if-one-string-is-a-subsequence-of-another
'''
def isSubseq(s, t):
    it = iter(t)
    return all(c in it for c in s)



'''
Return the largest index i such that s[:i] is a subsequence of t.
'''
def maxSubseq(s, t):
    it = iter(t)
    return next((i for i,c in enumerate(s) if c not in it), len(s))
