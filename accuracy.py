
from write_like import WriteLike
from difflib import Differ
import glob
import argparse



def my_diff(filename1,filename2, output_filename, author, lesk):
	file1 = open(filename1, 'r').read().strip().split()
	file2 = open(filename2, 'r').read().strip().split()

	pluses = 0
	minuses = 0
	differences = list(Differ().compare(file1,file2))
	for item in differences:
		if item[0] == '+':
			pluses += 1
		if item[0] == '-':
			minuses += 1

	return (pluses, minuses)

if __name__ == '__main__':

	o_file = 'output.txt'

	parser = argparse.ArgumentParser()
	parser.add_argument('-ouput_filename', '-o','--output_filename', type = str, 
						help = 'output file name', 
						required = False, default='results.txt')

	parser.add_argument('-test_directory', '-t', '--test_directory', type = str,
						required = True)
	parser.add_argument('-iterations', '-i', type = int, default = 100, 
						required = False)
	args = parser.parse_args()

	authors = ['dickens', 'hemingway', 'shakespeare', 'rappers']
	test_files = glob.glob(args.test_directory + '/*')

	print "Gathering test files..."

	temp_array_nolesk = []
	temp_array_lesk = []
	f = open(args.output_filename, 'w')
	f.write('TEST DETAILS\nITERATIONS: ' + str(args.iterations) + '\n')
	f.write('AUTHORS TESTED: ' + str(authors) + '\n')
	f.write('FILES: ' + str(test_files) + '\n')
	f.write('FILE DETAILS:\n')

	# write test file details
	for test_file in test_files:
		tf = open(test_file, 'r')
		f.write(test_file + ': ' + str(len(tf.read().split() ) ) + 'words\n')
		tf.close()

	# testing
	print "Starting tests..."

	for test_file in test_files:

		print "\tCurrently testing", test_file
		f.write('====\nFile: ' + test_file + '\n====\n')

		for author in authors:
			temp_array_nolesk = []
			temp_array_lesk = []

			for iteration in xrange(args.iterations):

				wl = WriteLike(author)

				wl.style_convert(infile_name = test_file, outfile_name = o_file)
				result = my_diff(test_file, o_file, args.output_filename, author, False)
				temp_array_nolesk.append(result)

				wl.style_convert_lesk(infile_name = test_file, outfile_name = o_file)
				result = my_diff(test_file, o_file, args.output_filename, author, True)
				temp_array_lesk.append(result)

			f.write('Author:' + author + '\t + (no lesk):' + str(1.0 * sum([plus[0] for plus in temp_array_nolesk])/len(temp_array_nolesk)) + '\n' )
			f.write('Author:' + author + '\t - (no lesk):' + str(1.0 * sum([minus[1] for minus in temp_array_nolesk])/len(temp_array_nolesk)) + '\n' )

			f.write('Author:' + author + '\t + (lesk)   :' + str(1.0 * sum([plus[0] for plus in temp_array_lesk])/len(temp_array_lesk)) + '\n')
			f.write('Author:' + author + '\t - (lesk)   :' + str(1.0 * sum([minus[1] for minus in temp_array_lesk])/len(temp_array_lesk)) + '\n' )

	f.close()
	print 'Done!'

