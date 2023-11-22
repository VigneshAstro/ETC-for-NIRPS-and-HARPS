def read_input_file(filename):
    # open the input file in read mode
    with open(filename, 'r') as f:
        # read the contents of the file
        contents = f.read()

    # create an empty dictionary to store the variable values
    variables = {}

    # split the contents of the file into individual lines
    lines = contents.split('\n')

    # loop through each line and extract the variable name and value
    for line in lines:
        # skip any empty lines or lines that do not contain an equals sign
        if not line or '=' not in line:
            continue

        # split the line into variable name and value
        name, value = line.split('=')

        # strip any leading or trailing whitespace from the variable name and value
        name = name.strip()
        value = value.strip()

        # convert the value to the appropriate data type
        if value.startswith("'"):
            value = value.strip("'")
        elif '.' in value:
            value = float(value)
        else:
            value = int(value)

        # add the value to the dictionary with the corresponding name
        variables[name] = value

    # return the dictionary of variables
    return variables
