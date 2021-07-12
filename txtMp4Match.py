import os
import glob
import argparse


def findUnMatched():
    parser = argparse.ArgumentParser(description = "TrainArgs");

    parser.add_argument('--mp4_dir', type=str, default="voxceleb2/dev/mp4", help='', required = True);
    parser.add_argument('--txt_dir', type=str, default="voxceleb2/dev/txt", help='', required = True);
    args = parser.parse_args();

    mp4files = glob.glob(args.mp4_dir+'/*/*/*.mp4')
    txtfiles = glob.glob(args.txt_dir+'/*/*/*.txt')
    print(len(mp4files), len(txtfiles))
    expected_txtfiles = [fname.replace(args.mp4_dir,args.txt_dir).replace('.mp4','.txt') for fname in mp4files]
    print(len(expected_txtfiles))


    toWrite = ''
    g = open('./syncnet_trainer/txtMp4NotMatched.txt','w')

    for i in expected_txtfiles:
        if i not in txtfiles:
            g.write(i + '\n')


def MatchTxtMp4():
    txtname = './syncnet_trainer/txtMp4NotMatched.txt'
    f = open(txtname,'r')
    txt = f.readlines()
    f.close()

    paths = []

    for eachLine in txt:
        temp = eachLine.split('/')[:-1]
        txtPath = ''
        for i in temp:
            txtPath += '/' + i

        if txtPath not in paths:
            paths.append(txtPath)

    for txtPath in paths:
        txtNames = sorted(os.listdir(txtPath))
        vidNames = sorted(os.listdir(txtPath.replace('txt','mp4')))
        print(txtPath)
        print(txtNames)
        print(vidNames)
        for i in range(len(txtNames)):
            txtName = txtNames[i]
            newTxtName = vidNames[i].replace('mp4','txt')

            g = open(os.path.join(txtPath,txtName),'r')
            txt = g.readlines()
            g.close()

            towrite=''
            for line in txt:
                towrite += line

            h = open(os.path.join(txtPath,newTxtName),'w')
            h.write(towrite)
            h.close()


def main():
    findUnMatched()
    MatchTxtMp4()
    
    
if __name__ == "__main__":
    main()
