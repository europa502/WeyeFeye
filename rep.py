import csv


count_matrix=[[0 for x in range(90,170)] for y in range(50,170)]

plots={}
for points_y in range(90,170):
	plots.setdefault(points_y,[])
	for points_x in range(50,170):
		plots[points_y].append(0)
#for x in plots:
	#print x,plots[x]

#plots.setdefaults()
with open('/root/weyefeye/data/data1.csv') as csv_file:
	csv_read=csv.reader(csv_file,delimiter=',')
	for lines in csv_read:
		try:
			print lines[2],lines[3],lines[4]
			plots[int(lines[3])][int(lines[4])-50]=int(lines[2])
			count_matrix[int(lines[3])][int(lines[4])]+=1				
			#print plots[int(lines[3])][int(lines[4])-50]
		except:
			continue
	for y in plots:
		print y,plots[y],"\n"
		print "counts", len(count_matrix),len(plots)
		
		print "\n"
	#print plots[113],plots[113][93]
	for point in range(0,170):
		print point, count_matrix[point]	
