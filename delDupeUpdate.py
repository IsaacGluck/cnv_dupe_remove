#!/usr/bin/env python

import sys, operator, csv, argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", type=str, help="The file that contains the data to be analyzed.")
parser.add_argument("-a", "--all", action="store_true", help="Display all the new data")
parser.add_argument("-l", "--lines", type=int , help="Display a certain number of lines from the new dataset")
parser.add_argument("-w", "--write", type=str, help="Writes new data to a new specified file.")
args = parser.parse_args()

data = []
try:
	with open(args.file, "r") as tsvfile:
		reader = csv.reader(tsvfile, delimiter="\t")
		for row in reader:
			data.append(row)
except IOError:
	print "There was a problem opening " + args.file

header = data[0]
header.append('Number')
header.append('Duplicates')
header.append('Identical')

data = data[1:]
data = sorted(data, key=operator.itemgetter(1,2))

#Give every datum a number to be referenced from
counter = 1
for i in data:
	i.append(str(counter))
	i.append('')
	i.append('')
	counter+=1

def overlap(l1, l2):
	if l1[1]-l1[0] > l2[1]-l2[0]:
		big = l1
		small = l2
	else:
		big = l2
		small = l1

	b0 = big[0]
	b1 = big[1]
	s0 = small[0]
	s1 = small[1]

	#If one is inside the bigger
	if b0 <= s0 and b1 >= s1:
		return True

	#If one is totally out of the bounds of the bigger
	elif (s1 <= b0) or (s0 >= b1):
		return False

	#If it is partially inside, check if it's more than 50%
	elif s0 < b0 and s1 > b0 and s1 < b1:
		if (s1-b0) >= (b0-s0):
			return True
		else:
			return False
	elif s0 > b0 and s0 < b1 and s1 > b1:
		if (b1-s0) >= (s1-b1):
			return True
		else:
			return False

def identical(l1, l2):
	if l1 == l2:
		return True
	else:
		return False

#Make the chromosome intervals ints
for i in data:
	i[2] = int(i[2])
	i[3] = int(i[3])

#Find Duplicates
for i in data:
	current = data.index(i)
	lenChr = i[3]-i[2]

	#Compares all values after the current value
	for n in data[current + 1:]:
		lenChrCompare = n[3]-n[2]

		if lenChr > lenChrCompare:
			small = n
			big = i
		else:
			small = i
			big = n

		#Same Chromosomes
		if i[1] == n[1]:

			#If they are identical
			if identical([i[2],i[3]], [n[2], n[3]]):
				if i[8] == '':
					i[8] = 'Identical to ' + str(n[6])
				else:
					i[8] += ' , ' + str(n[6])
				if n[8] == '':
					n[8] = 'Identical to ' + str(i[6])
				else:
					n[8] += ' , ' + str(i[6])
	
				#Different Sources
			if i[0] != n[0]:

				#If the overlap is greater than 50%
				if overlap([i[2],i[3]], [n[2], n[3]]):
					if small[7] == '':
						small[7] = 'Dup of: ' + str(big[6])
					else:
						small[7] += ' , ' + str(big[6])

#Make the chromosome intervals back into strings
for i in data:
	i[2] = str(i[2])
	i[3] = str(i[3])

# Writes the new data to a seperate file
# args_dict = vars(args)
if args.write != None:
	try:
		new = open(args.write, "w")
		new.write("\t".join(header) + "\n")
		for i in data:
			new.write("\t".join(i) + "\n")
	except IOError:
		print "Could not write to" + args.write

counter = 0;
for i in data:
	output="\t".join(i)+"\n"
	if (not args.all and counter >= 20):
		break
	elif args.lines!= None and args.lines<=counter:
		break
	else:
		sys.stdout.write(output)
		counter+=1










