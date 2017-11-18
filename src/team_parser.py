class team_parser:
    # Convert the team 3 letter code to a 6 digit number for easier processing
    def str_to_nb(self, _arg):
        out = []
        for i in range(0, len(_arg)):
            # Get the ASCII value of the character, as a string
            nb_str = str(ord(_arg[i]))
            for j in range(0, len(nb_str)):
                # Add each character of the string to the output list
                out.append(int(nb_str[j]))
        # Return the resulting list, converted to an int
        return int(''.join(str(x) for x in out))

    # Convert the 6 digit number back to a 3 letter code
    def nb_to_str(self, _arg):
        out = []
        ctr = 0 # Initialize a counter for indexing the 6 digit int
        for i in range(0, 3):
            _str = []
            _str.append(_arg[ctr])
            _str.append(_arg[ctr + 1])
            ctr += 2
            # create a string, convert it to int and append correspond character to string
            out.append(chr(int(''.join(str(x) for x in _str))))
        return ''.join(out)
