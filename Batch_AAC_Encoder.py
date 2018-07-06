#
#
# This code will convert any .wav files in the same directory as the script
# to AAC, in a .m4a container
# It lets you specify if you want CBR and/or VBR encoding, and also the bitrate
# It only works for input files without spaces.  I will try to update to allow
# for any filenames in the future
#
#
# Greg McAllister
# version 1 - 04 June 2018
# version 2 - 05 June 2018 - added progeress reporting, which is nice for large file lists
#   also removed list defining function - only called it once so no need for function really
#

import os
import shutil

# warning for use case
print "\nNote this only (currently) works for filenames without any spaces!\n"

# user input for selecting parameters (with some error checking)
print "Would you like CBR conversion? (y/n)"
CBR_query = raw_input()
while CBR_query != 'y' and CBR_query != 'n':
    print "Invalid input.  Would you like CBR conversion? (y/n)"
    CBR_query = raw_input()

print "Would you like VBR conversion? (y/n)"
VBR_query = raw_input()
while VBR_query != 'y' and VBR_query != 'n':
    print "Invalid input.  Would you like VBR conversion? (y/n)"
    VBR_query = raw_input()

if VBR_query == 'n' and CBR_query == 'n':
    print "Closing with no processing"
    exit()

print "What bitrate would you like? (type number of bits, not kilobits)"
bitrate = raw_input()
while not bitrate.isdigit() or int(bitrate) > 320000 or int(bitrate) < 16000:
    print "Bitrate needs to be a whole number between 16000 and 320000. What bitrate would you like?"
    bitrate = raw_input()

# sort out the various bitrate parameters for later use and renaming
bitrate = int(bitrate)
bitrate_to_print = str(bitrate/1000)+'k'

# sort out the file list (more complex selection that just = os.listdir(path))
path = os.getcwd()
FileList = []
for f in os.listdir(path):
    if not f.startswith('.') and ".wav" in f:
        FileList.append(f)

print "Progress:"

# Actual processing
if CBR_query == 'y':
    os.mkdir('CBR')

    print "Processing CBR conversions"
    i = 1

    for infile in FileList:
        outfile = "%s_AAC_CBR_%s.m4a" % (infile[:-4], bitrate_to_print)
        # -s 0 is flag for CBR
        os.system("afconvert %s %s -f m4af -d aac -s 0 -b %d" % (infile, outfile, bitrate))
        # move to correct directory
        shutil.move(outfile, path+'/CBR')

        print "%d: File '%s' completed\n" % (i, infile)
        i+=1

    print "CBR conversions completed\n"

# could add flag --soundcheck-generate to add soundcheck data to output file...
# maybe add option at some point if deemed useful

if VBR_query == 'y':
    os.mkdir('VBR')

    print "Processing VBR conversions"
    i = 1

    for infile in FileList:
        outfile = "%s_AAC_VBR_%s.m4a" % (infile[:-4], bitrate_to_print)
        # -s 2 is flag for VBR (constrained), rather than full on VBR
        os.system("afconvert %s %s -f m4af -d aac -s 2 -b %d" % (infile, outfile, bitrate))
        # move to correct directory
        shutil.move(outfile, path+'/VBR')

        print "%d: File '%s' completed\n" % (i, infile)
        i+=1

    print "VBR conversions completed\n"

# maybe put some error reporting in here.... at least it works for now
