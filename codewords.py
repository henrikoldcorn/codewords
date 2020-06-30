import time, functools
from memoization import cached

file = open(r"C:\Users\Henrik\Documents\code\python\wordlist.txt")
wordlist = sorted(list(set([x[:-1].lower() for x in file])))

def translate(word, alphabet):
    value = ""
    for letter in word:
        if letter in alphabet:
            value += alphabet[letter]
        else:
            value += "0"
    return value

def full(alphabet):
    for i in range(1, 27):
        if i not in alphabet:
            return False
    return True

def match(code, word, alph): #list of numbers, string, dict
    if len(code) != len(word):
        return False
    temp_alph = alph.copy()
    
    for i in range(len(code)):
        n, l = code[i], word[i]
        if n in temp_alph:
            if temp_alph[n] != l:
                return False
        elif l in temp_alph.values():
            return False
        else:
            temp_alph[n] = l
    return True

@cached(thread_safe=False)
def possible_words(code, alph):
    result = []
    for i in wordlist:
        if len(i) == len(code) and match(code, i, alph):
            result.append(i)
    return result

def update(alph, numbers, letters): #list, list, string
    temp_alph = alph.copy()
    if len(numbers) != len(letters):
        print("len error", numbers, letters)
    for i in range(len(numbers)):
        n, l = numbers[i], letters[i]
        if n not in temp_alph:
            temp_alph[n] = l
    return temp_alph

def codeword(words, alph): #(list of unsolved words in crossword, dict,
    temp_alph = alph.copy()
    #success conditions
    if len(words) == 0:
        return temp_alph
    """
    possibles = possible_words(words[0], temp_alph)
    #failure condition
    if possibles == []:
        return False
    """
    if full(temp_alph):
        return temp_alph
    
    for code in words:
        possibles = possible_words(code, temp_alph)
        #failure condition
        if len(possibles) == 0:
            return False
        
        for test in possibles:
            #assume test is correct, so recurse with updated dict
            value = codeword(words[1:], update(temp_alph, code, test))
            #if it worked, we have soln, else try the next one
            if value:
                return value

def score(words, alph):
    t_words = words.copy()
    t_alph = alph.copy()
    s = 0
    for i in t_words:
        if i in t_alph:
            s += 1
    return s
        
def solve(words, alph=None):
    if alph is None:
        alph = {}
        
    #sort words for better speed
    t_words = sorted(words, key=lambda i: score(i, alph), reverse=True)
    
    alph = codeword(words, alph)
    print(alph)
    for i in words:
        print(i, translate(i, alph))

#test
#wordlist = ["cabbies", "dabbing", "yummier", "dolt"]

unsolved = [ [11, 13, 16, 16, 10, 26, 1],
             [21, 10, 16, 6, 13, 1, 2],
             [16, 12, 8, 19, 7, 10, 20, 12, 4],
             [17, 12, 21, 6, 5],
             [17, 20, 20, 14],
             [3, 20, 17, 17, 2, 15, 16, 13, 17, 17],
             [2, 26, 24, 15, 8, 2],
             [26, 2, 23, 17, 15, 23, 2, 9],
             [9, 10, 4, 18, 12, 13, 17, 10, 25, 15],
             [8, 2, 4, 13],
             [2, 26, 26, 12, 10],
             [6, 5, 10, 21, 20, 19, 20, 9, 15],
             [7, 2, 13, 4, 5, 20, 19],
             [8, 10, 17, 10, 2, 12, 22],
             [11, 12, 16, 10, 17, 2, 2],
             [20, 9, 9, 8, 2, 26, 7],
             [16, 13, 8, 16, 20, 20, 24, 17, 2],
             [4, 2, 26, 26, 13],
             [10, 20, 7, 13],
             [13, 8, 13, 7, 2, 12, 21, 10, 4, 5],
             [1, 26, 20, 8, 20, 26],
             [4, 14, 12, 17, 17, 6, 13, 19],
             [21, 2, 4, 20, 17, 3, 2, 9],
             [13, 25, 25, 10, 21, 8],
             [16, 2, 17, 17, 15, 25, 17, 20, 19, 4],
             [11, 20, 23, 17],
             [13, 20, 21, 7, 13],
             [23, 20, 2, 16, 2, 1, 20, 26, 2],
             [2, 22, 5, 13, 17, 2, 9],
             [19, 5, 13, 21, 15, 26, 22]
             ]

start = time.time()
solve(unsolved, {3:"v", 20:"o", 17:"l"})
print(time.time()-start, "seconds")
