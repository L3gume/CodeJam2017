class team_parser:
    def str_to_nb(_arg):
        out = []
        for i in range(0, len(_arg)):
            nb_str = str(ord(_arg[i]))
            for j in range(0, len(nb_str)):
                out.append(int(nb_str[j]))
        return int(''.join(str(x) for x in out))

    def nb_to_str(_arg):
        out = []
        ctr = 0
        for i in range(0, 3):
            _str = []
            _str.append(_arg[ctr])
            _str.append(_arg[ctr + 1])
            ctr += 2
            out.append(chr(int(''.join(str(x) for x in _str))))
        return ''.join(out)
