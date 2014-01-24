import operator, csv


data = []
with open("recurrent_cnv.CNV.tsv", "r") as tsvfile:
	reader = csv.reader(tsvfile, delimiter="\t")
	for row in reader:
		data.append(row)

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

for i in data:
	i[2] = str(i[2])
	i[3] = str(i[3])


new = open("Marked.tsv", "w")
new.write("\t".join(header) + "\n")
for i in data:
	new.write("\t".join(i) + "\n")








