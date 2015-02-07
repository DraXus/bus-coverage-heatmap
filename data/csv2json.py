import sys
import csv

def parse(line, easy):
	if easy:
		return (line[0], line[1], line[2], line[3])
	else:
		return (line[0], line[3], line[4], line[5])

if len(sys.argv)<2:
	print '**** Syntax: csv2json.py inputfile.csv [header] [easy-format] > outputfile.json'
	exit()


if len(sys.argv)<3:
	header = False
else:
	header = True if sys.argv[2]=='1' else False


if len(sys.argv)<4:
	easy = False
else:
	easy = True if sys.argv[3]=='1' else False

inputfile = sys.argv[1]

f = open(inputfile, 'r')
r = csv.reader(f)
if header:
	next(r, None)

s = '{"max": 4, "data": ['
for line in r:
	s = s + '{"code": "%s", "lng": %s, "lat": %s, "name": "%s", "count": 1}, ' % parse(line, easy)

s = s[0:len(s)-2]+"]}"
print(s)
