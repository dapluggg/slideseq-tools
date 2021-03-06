#!/usr/bin/python

# This script is to generate library_params.txt that is needed by converting Illumina basecalls to sam

import sys
import getopt
import csv

def main(argv):
    inputfile = ''
    outputfile = ''
    bamfolder = ''
    name = ''
    lane = ''
    try:
        opts, args = getopt.getopt(argv,"hi:o:b:n:l:",["ifile=","ofile=","bfolder=","name=","lane="])
    except getopt.GetoptError:
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-b", "--bfolder"):
            bamfolder = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-l", "--lane"):
            lane = arg
            
    fout = open(outputfile,'w')
    title = 'OUTPUT\tSAMPLE_ALIAS\tLIBRARY_NAME\tBARCODE_1\n';
    fout.write(title)

    with open(inputfile, 'r') as fin:
        reader = csv.reader(fin, delimiter='\t')
        idx_LANE = -1
        idx_SAMPLE = -1
        idx_LIBRARY = -1
        idx_SAMPLE_BARCODE = -1
        i = 1
        for row in reader:
            if (i == 1):
                if ('lane' in row):
                    idx_LANE = row.index('lane')
                if ('sample' in row):
                    idx_SAMPLE = row.index('sample')
                if ('library' in row):
                    idx_LIBRARY = row.index('library')
                if ('sample_barcode' in row):
                    idx_SAMPLE_BARCODE = row.index('sample_barcode')
            else:
                if (row[idx_LANE] != lane):
                    continue
                str = bamfolder+row[idx_LIBRARY]+'/'
                if (row[idx_SAMPLE_BARCODE]):
                    str += row[idx_SAMPLE_BARCODE]+'/'+name+'.'+row[idx_LIBRARY]+'.'+row[idx_SAMPLE_BARCODE]+'.unmapped.bam\t'
                else:
                    str += name+'.'+row[idx_LIBRARY]+'.unmapped.bam\t'
                if (idx_SAMPLE >= 0):
                    str += row[idx_SAMPLE] + '\t'
                else:
                    str += '\t'
                if (idx_LIBRARY >= 0):
                    str += row[idx_LIBRARY] + '\t'
                else:
                    str += '\t'
                if (idx_SAMPLE_BARCODE >= 0):
                    str += row[idx_SAMPLE_BARCODE] + '\n'
                else:
                    str += '\n'
                fout.write(str)
            i = i + 1

    fin.close()
    fout.close()


if __name__ == "__main__":
   main(sys.argv[1:])

