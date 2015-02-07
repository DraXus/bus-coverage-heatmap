import csv
f = open('bournemouth_simplified.csv', 'r')
r = csv.reader(f)

s = '{"max": 4, "data": [';
for line in r:
	s = s + '{"code": "%s", "lng": %s, "lat": %s, "name": "%s", "count": 1}, ' % (line[0], line[1], line[2], line[3]);

s = s+"]}"
print(s)
