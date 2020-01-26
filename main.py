from os import walk
import util
import re
import sys

print sys.argv

dir = 'images'

if len(sys.argv) > 1:
    dir = sys.argv[1]

for (dirpath, dirnames, filenames) in walk('./'+sys.argv[1]):
    # if on MAC, rmeove .DS_Store file
    if '.DS_Store' in filenames:
        filenames.remove('.DS_Store')
    # We want the files to be sorted based on page number
    # name = shingeki_no_kyojin_72_18.jpg
    # split('_'), get the last part , then extract number

    file_list = []
    indice_list = []
    back = bool(False)

    if 'cover.jpg' in filenames:
        filenames.remove('cover.jpg')
        file_list.append(dirpath+'/'+'cover.jpg')

    if 'back.jpg' in filenames:
        filenames.remove('back.jpg')

    for i, s in enumerate(filenames):
        z = re.search('[0-9]{3}', s)
        # print z.
        if z:
            indice_list.append((int(z.group(0)), i))
        # filenames[i] =

    # filenames = sorted(filenames,key=lambda name:int(name.split('_')[::-1][0].split('.')[0]))
    indice_list = sorted(indice_list, key=lambda x: x[0])

    for index, i in enumerate(indice_list):
        file_list.append(dirpath+'/'+filenames[i[1]])

    if back == True:
        file_list.append(dirpath+'/'+'back.jpg')

    # print file_list
    print "Working For :", dirpath, "(", len(file_list), "pages)"
    util.make_pdf(dirpath, file_list)
