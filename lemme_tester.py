import sys
import pymorphy2
import json
import csv

'''Neatly prints output of json lemme files to out_test.txt'''

def main():
    try:
        filename = sys.argv[1]
    except FileNotFoundError and IndexError:
        filename = "outHyphenOct28.json"
    myfile = open(filename, mode='r')

    print(filename)
    table = json.load(myfile)
    outfile = open('out_test.txt', 'w')
    count = 1
    for row in table:
        outString = str(count) + ") "
        for item in row:
            outString += str(item) + ", "
        outfile.write(outString + '\n\n')
        count += 1
    outfile.close()


main()
