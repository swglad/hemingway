f = open('imjustgonnashake.txt','r')

shake_dict={}

for line in f:
	temp = line.split(':')
	if len(temp[0].split())==1 and len(temp[1].split())==1:
		shake_dict[temp[0].strip().lower()] = temp[1].split('.')[0].strip().lower()

f.close()

s = open('shakespeare_mapfile.txt','w')

for item in shake_dict:
	s.write(str(item)+'\t'+shake_dict[item]+'\n')

s.close()