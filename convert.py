import sys
import getopt
from gmshtoparticles import mesh

def main(argv):
        
    path = ''
    output = ''
    outtype = ''
    norm = 0
    print_id = True
    rotate = 0
    helpText = "convert.py -i <inputfile> -o <outputfile> -t <type>\n"
    if len(sys.argv) <= 4:
        print(helpText)
        sys.exit(1)

    try:
        opts, args = getopt.getopt(
        argv, "hi:o:t:n:d:r:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print(helpText)
        sys.exit(0)

    for opt, arg in opts:
        if opt == '-h':
            print (helpText)
            sys.exit(0)
        elif opt in ("-i", "--ifile"):
            path = arg
        elif opt in ("-o", "--ofile"):
            output = arg
        elif opt in ("-t", "--type"):
            outtype = arg
        elif opt in ("-n", "--normalize"):
            norm = int(arg)
        elif opt in ("-d", "`--print_id"):
            print_id = int(arg)
        elif opt in ("-r", "`--rotate"):
            rotate = float(arg)
               
               
    mesh.GmshToParticles(outtype, path, output, print_id, norm, rotate)

if __name__ == "__main__":
    main(sys.argv[1:])    
