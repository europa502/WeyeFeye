import csv
import numpy as np
import scipy.misc as smp
csv_file=open('data1.csv','r')
csv_reader=csv.reader(csv_file, delimiter=',')
a={}
next(csv_reader)
for lines in csv_reader:
    key=str(lines[4])+'.'+str(lines[3])
    if key not in a:
        a.setdefault(key,[])
        a[key].append(int(lines[2]))
        a[key].append(1)
    if key in a:
        a[key][0]=a[key][0]+int(lines[2])
        a[key][1]=a[key][1]+1

# Create a 200x200x3 array of 8 bit unsigned integers
data = np.zeros( (200,200,3), dtype=np.uint8 )

for key in a:
    a[key][0]=float(a[key][0])/(float(a[key][1]))/(-90)
    print key,a[key]
    data[int(key.split('.')[0]),int(key.split('.')[1])] = [int(a[key][0]*255),int(a[key][0]*255),int(a[key][0]*255)]

img = smp.toimage( data )       # Create a PIL image
img.show()
