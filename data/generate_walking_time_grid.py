import subprocess
import json
import sys

def create_grid(lat, lng):
	print "Generating grid for %s %s" % (lat,lng)
	grid = []
	iterations = 10 # number of points in each direction (N, S, E, W)
	step = 0.00001
	
	for i in xrange(0, iterations):
		point_N = {"lat": lat+step, "lng": lng}
		point_S = {"lat": lat-step, "lng": lng}
		point_E = {"lat": lat, "lng": lng+step}
		point_W = {"lat": lat, "lng": lng-step}
		point_NE = {"lat": lat+step, "lng": lng+step}
		point_SE = {"lat": lat-step, "lng": lng+step}
		point_NW = {"lat": lat+step, "lng": lng-step}
		point_SW = {"lat": lat-step, "lng": lng-step}
		step = step+step
		grid.append(point_N)
		grid.append(point_S)
		grid.append(point_E)
		grid.append(point_W)
		grid.append(point_NE)
		grid.append(point_SE)
		grid.append(point_NW)
		grid.append(point_SW)

	return grid

def parse_time(output): # dirty parsing...
	temp = output.split(',')
	temp = temp[1].split(" ")
	return temp[1]

def generate_json(grid, outputfile):
	f = open(outputfile, 'w')
	s = '{"max": 0, "data": ['
	for point in grid:
		s += '{"lng": %s, "lat": %s, "count": -%s}, ' % (point["lng"], point["lat"], point["walking_time"])
	s = s[0:len(s)-2]+"]}"
	f.write(s)
	f.close()

if len(sys.argv)<3:
	print "**** Syntax: generate_walking_time_grid.py input_file.json output_file.json"

inputfile = sys.argv[1]
outputfile = sys.argv[2]

f = open(inputfile, 'r')
json_input = json.load(f)
bus_stops = json_input["data"]
#bus_stops = bus_stops[0:20]
print "Processing %s bus stops" % len(bus_stops)

routino_call = "/var/www/routino/bin/router --dir=/var/www/routino/data/ --lon1=%s --lat1=%s --lon2=%s --lat2=%s --quickest --transport=foot --output-gpx-route --output-stdout | grep \"Total Journey\""

supergrid = []
# iterate over bus stops to compute walking time
for b in bus_stops:
	grid = create_grid(b["lat"], b["lng"])
	to_remove = []
	for i in xrange(0, len(grid)):
		point = grid[i]
		try:
			routino_output = subprocess.check_output(routino_call % (point["lng"], point["lat"], b["lng"], b["lat"]), stderr=subprocess.STDOUT, shell=True)
			grid[i]["walking_time"] = parse_time(routino_output)
			supergrid.append(grid[i])
		except:
			print 'Cannot find route, removing point from grid' # probably the point is not accesible (in the sea)


print "Supregrid size = %s" % len(supergrid)

# generate json output
generate_json(supergrid, outputfile)


