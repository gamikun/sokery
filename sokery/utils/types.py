import sys

portrange = lambda up, low: (int(up), int(low))


def portlist(x):
    strings = x.split(',')
    ports = []

    for s in strings:
        if '-' in s:
            rng = tuple([int(x) for x in s.split('-', 1)])
            ports.append(rng)
        else:
            ports.append(int(s))

    return ports


if __name__ == '__main__':
    lst = portlist('1000,2000-5000,500-550')
    print(lst)

