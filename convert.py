from gmshtoparticles import mesh
import sys
import getopt

def main(argv):
        
    path = ''
    output = ''
    outtype = ''
    norm = 0
    helpText = "convert.py -i <inputfile> -o <outputfile> -t <type>\n"
    if len(sys.argv) <= 4:
        print(helpText)
        sys.exit(1)

    try:
        opts, args = getopt.getopt(
            argv, "hi:o:t:n:", ["ifile=", "ofile="])
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
               
               
    mesh.GmshToParticles(outtype, path, output,norm)

if __name__ == "__main__":
    main(sys.argv[1:])    
