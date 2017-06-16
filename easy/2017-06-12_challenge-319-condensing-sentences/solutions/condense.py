#!/usr/bin/env python3


def main():
    with open('input.txt') as f_in:
        for line in f_in.readlines():
            print(condense(line.strip()))


def condense(sentence):
    condensed = []
    tokens = list(reversed(sentence.split(' ')))
    while len(tokens) > 1:
        first, second = tokens.pop(), tokens.pop()
        similarity = max(
            (i for i in range(1, min(len(first), len(second)) + 1) if second.startswith(first[-i:])),
            default=0)
        if similarity:
            tokens.append('{}{}'.format(first, second[similarity:]))
        else:
            condensed.append(first)
            tokens.append(second)

    condensed.extend(tokens)
    return ' '.join(condensed)


if __name__ == '__main__':
    main()
