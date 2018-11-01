input_file = "mapServer.py"  # e.g. source.py
output_file = "output"  # e.g out.py
with open(input_file, 'r') as source:
    with open(output_file, 'a+') as result:
        for line in source:
            line = line.replace('\t', '    ')
            result.write(line)
