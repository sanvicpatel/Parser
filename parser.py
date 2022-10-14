import nltk
import sys

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S 
AJP -> Adj NP 
ADP -> VP Adv | Adv VP 
NP -> N | Det N | Det AJP | AJP | P NP 
VP -> V | VP NP | VP Conj VP | ADP  
"""

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    # Tokenize sentence
    words = nltk.word_tokenize(sentence)

    # Loop through length(words) number of times
    word = 0
    while word < len(words):
        # Make the word lowercase
        words[word] = words[word].lower()

        # Set number of alphabetical letters = 0
        num_letters = 0

        # Traverse through word and count number of alphabetical letters
        for letter in words[word]:
            if letter.isalpha():
                num_letters += 1

        # If number of alphabetical letters is 0, remove the word
        if num_letters == 0:
            words.remove(words[word])
            continue

        word += 1

    return words


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    # Empty list of np chunks
    noun_phrase_chunks = []

    # Traverse through every subtree
    for subtree in tree.subtrees():
        # If the subtree is an NP and it has a height of 3, it is a np chunk
        if subtree.label() == "NP" and subtree.height() == 3:
            noun_phrase_chunks.append(subtree)

    # Return list
    return noun_phrase_chunks


if __name__ == "__main__":
    main()
