"""
Script to parse the results given in JSON format
"""
import sys
import json

try:
    file = sys.argv[1]
    with open(file, encoding='utf-8') as data_file:
        data = json.loads(data_file.read())
    data = data['critiques']['680']['rubric_items']['5510']['observation']
    data = data.replace('. ', '\n')
    data = data.replace('\n', '\n')

    print(data)

    file = open('result.txt','w')
    file.write(data)
    file.close()

except json.decoder.JSONDecodeError:
    print("Enter a valid filename argument")
