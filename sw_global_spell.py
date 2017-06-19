"""Run spellcheck on input words."""
import sys


class Score(object):
    """Store scoring parameters."""

    def __init__(self, match, mismatch, gap):
        """Initialize scoring parameters."""
        self.match = match
        self.mismatch = mismatch
        self.gap = gap

    def printer(self):
        """Print scoring parameters."""
        print("(" + str(self.match)
              + ", " + str(self.mismatch)
              + ", " + str(self.gap) + ")")


def make_matrix(xdim, ydim, penalty):
    """Return a matrix filled with zeroes."""
    A = [[0 for x in range(xdim)] for y in range(ydim)]
    for ii in range(xdim):
        A[0][ii] = ii * penalty
    for ii in range(ydim):
        A[ii][0] = ii * penalty
    return A


def local_align(x, y, score):
    """Return the best score for local alignment between two strings."""
    A = make_matrix(len(x) + 1, len(y) + 1, score.mismatch)
    best = 0

    for ii in range(1, len(y) + 1):
        for jj in range(1, len(x) + 1):
            n1 = A[ii][jj - 1] + score.gap
            n2 = A[ii - 1][jj] + score.gap
            if x[jj - 1] == y[ii - 1]:
                n3 = A[ii - 1][jj - 1] + score.match
            else:
                n3 = A[ii - 1][jj - 1] + score.mismatch

            A[ii][jj] = max(n1, n2, n3)

    best = A[len(y)][len(x)]
    return best


def get_words(fn):
    """Read words from a plain text file."""
    with open(fn) as f:
        words = f.readlines()
    return([word.strip() for word in words])


def the_best_words(strang, fn, score):
    """Print the result of checking a list of common words against input."""
    words = get_words(fn)
    best = 0
    best_words = []
    for word in words:
        t = local_align(strang, word, score)
        if word == strang:
            t = best
            if len(best_words) > 0:
                best_words.clear()
            best_words.append(word)
            break
        if t > best:
            best = t
            if len(best_words) > 0:
                best_words.clear()
        if t == best and best > 0:
            best_words.append(word)

    if best == 0:
        print("NO SUGGESTIONS")
    if len(best_words) == 1:
        print(best_words[0].upper())
    if len(best_words) > 1:
        for ii in range(len(best_words)):
            best_words[ii] = best_words[ii].upper()
        # for a more friendly interface, uncomment below:
        # print("Did you mean any of the following words?")
        # for word in best_words:
            # print(word.upper())
        print(best_words)
#    if you want to see the score, uncomment this
#    print("score: " + str(best))
    return(best_words, best)


if len(sys.argv) > 1:
    s1 = sys.argv[1].lower()
    for c in s1:
        if not c.isalpha():
            s1 = s1.replace(c, "")
else:
    s1 = ""

if len(sys.argv) > 2:
    fn = sys.argv[2]
else:
    fn1 = "PythonAutoWeb/static/resources/commonWords.txt"
    fn2 = "./commonWords.txt"

if len(sys.argv) > 5:
    n1 = int(sys.argv[3])
    n2 = int(sys.argv[4])
    n3 = int(sys.argv[5])
    score = Score(n1, n2, n3)
else:
    score = Score(2, -1, -2)

try:
    the_best_words(s1, fn1, score)
except Exception:
    the_best_words(s1, fn2, score)
