import sys

alphabet = "abcdefghijklmnopqrstuvwxyz"


def load_words(path):
    with open(path) as f:
        raw = f.read()
    words = raw.lower().split("\n")
    words = filter(lambda w: len(w) > 0, words)
    for w in words:
        for c in w:
            if c not in alphabet:
                raise Exception("Word \"{}\" contains invalid character '{}'.".format(w, c))
    return words


def calc_anagrams(words):
    ret = {}
    for w in words:
        s = ''.join(sorted(w))
        if s not in ret:
            ret[s] = [w]
        else:
            ret[s].append(w)
    return ret


def recur(used, found, potentials, anagrams):
    if len(potentials) == 0 and len(''.join(found)) >= threshold:
        print len(''.join(found)), ", ".join([" ".join(anagrams[f]) for f in sorted(found)])

    for i, w in enumerate(potentials):
        if len(found) == 0:
            if 'q' not in w:
                continue
        if len(found) == 1:
            if 'z' not in w and 'z' not in found[0]:
                continue

        u = used.union(w)
        f = found + [w]
        p = filter(lambda p: len(u.union(set(p))) == len(u) + len(p), potentials[i + 1:])
        recur(u, f, p, anagrams)


def find_pangrams(path):
    print "Loading words from", path
    words = load_words(path)
    print len(words), "words"
    words = filter(lambda w: len(w) == len(set(w)), words)
    print len(words), "with unique letters"
    anagrams = calc_anagrams(words)
    words = anagrams.keys()
    words = special_order_words(words)
    print len(words), "anagrams"

    recur(set(), [], words, anagrams)


def special_order_words(words):
    q, rest = separate_by(words, 'q')
    z, rest = separate_by(rest, 'z')
    return sorted(q) + sorted(z) + sorted(rest)


def separate_by(words, ch):
    has = []
    hasnot = []
    for w in words:
        if ch in w:
            has.append(w)
        else:
            hasnot.append(w)
    return has, hasnot


def main():
    global threshold
    threshold = int(sys.argv[1])
    path = sys.argv[2]
    find_pangrams(path)


main()
