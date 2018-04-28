
def portlist(x):
    strings = x.split(',')
    integers = [int(n) for n in strings]
    return list(set(integers))