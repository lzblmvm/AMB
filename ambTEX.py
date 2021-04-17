from os import listdir, walk, chdir
from blend_modes import darken_only, soft_light, dodge, overlay
from cv2 import imread, imwrite, merge, imshow, split, IMWRITE_JPEG_QUALITY, cv2, cvtColor, COLOR_RGB2BGR, COLOR_BGR2RGB
import numpy as np
from tkinter import END


class ambTEX(object):
    """
        Load images from the given directory and redy them for processing.
    """



    def __init__(self, dir, dirO, suffix, lb_logList):

        self.dir = dir
        self.dirO = dirO
        self.flist = []
        self.fDic = {}
        self.suff = suffix
        self.value = []
        self.lb_logList = lb_logList
        
        _, _, self.flist = next(walk(dir))

        for i in self.flist:

            key = self.getKey(i)
            
            if key not in self.fDic:

                self.fDic[key] = []         #Inserting new key.
                self.fDic[key].append(i)    #Adding value for the new key.

            else:

                self.fDic[key].append(i)

    

    def convert(self):

        for k in self.fDic.keys():
            
            composifn = self.getRef(k)
            setA = [None] * 8

            for i in range(len(composifn)):

                setA[i] = cv2.imread(composifn[i], -1).astype('float32')

            for j in range(len(setA)):

                if not self.hasAlpha(setA[j]):
                    
                    setA[j] = self.addAlpha(setA[j])

            img_out = darken_only(setA[5], setA[0], 1.0)
            #img_out = overlay(img_out, setA[0], 1.0)
            self.saveIMG(self.getFileName(composifn), img_out, self.dirO)
            #cv2.imshow('Output', img_out.astype(np.uint8))
            self.setLogs(k)
            
        return None



    def convert2(self):

        for k in self.fDic.keys():
            
            composifn = self.getRef(k)
            setA = [None] * 8

            for i in range(len(composifn)):

                setA[i] = cv2.imread(composifn[i], -1).astype('float32')

            for j in range(len(setA)):

                if not self.hasAlpha(setA[j]):
                    
                    setA[j] = self.addAlpha(setA[j])

            img_out = dodge(setA[5], setA[6], 1.0)
            img_out = overlay(img_out, setA[0], 1.0)
            self.saveIMG(self.getFileName(composifn), img_out, self.dirO)
            #cv2.imshow('Output', img_out.astype(np.uint8))
            self.setLogs(k)
                   
        return None


    
    def saveIMG(self, fname, img, dirO):
        
        chdir(dirO)

        #img = img[:, :, [2, 1, 0]]

        #img = img.astype('float32')
        #img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        img = self.rmAlpha(img)

        cv2.imwrite(dirO + fname, img, [cv2.IMWRITE_JPEG_QUALITY, 100])



    def addAlpha(self, img):

        b_chan, g_chan, r_chan = cv2.split(img)
        alpha_chan = np.ones(b_chan.shape, dtype=b_chan.dtype) * 50
        img = cv2.merge((b_chan, g_chan, r_chan, alpha_chan))

        return img



    def rmAlpha(self, img):

        img = img[:,:,:3]

        return img



    def hasAlpha(self, img):

        return img.shape[2] == 4


   
    def getRef(self, key):
        """
        Args:
            A key that represents a single UV set in 'fDic' dictionary.

        Returns:
            A list of address for texture in the below order: 
            [_co, _nohq, _as, _smdi, _ht, _spec, _gloss, _opgl] 
              0     1     2     3      4    5       6      7
        """

        target = self.fDic.get(key)
        temp = [None] * len(target)
        abs_dir = self.dir

        for i in target:

            i = i.lower()
            f = abs_dir + '/' + i

            if self.getType(i) == 0:
                temp[0] = f

            elif self.getType(i) == 1:
                temp[1] = f

            elif self.getType(i) == 2:
                temp[2] = f

            elif self.getType(i) == 3:
                temp[3] = f

            elif self.getType(i) == 4:
                temp[4] = f

            elif self.getType(i) == 5:
                temp[5] = f

            elif self.getType(i) == 6:
                temp[6] = f

            elif self.getType(i) == 7:
                temp[7] = f

            else:
                break
        
        return temp

        
    
    def getType(self, fname):

        ftype = fname[fname.rfind('_') : fname.rfind('.')]

        if ftype == '_co':
            return 0

        elif ftype == '_nohq':
            return 1

        elif ftype == '_as':
            return 2

        elif ftype == '_smdi':
            return 3

        elif ftype == '_ht':
            return 4

        elif ftype == '_spec':
            return 5

        elif ftype == '_gloss':
            return 6

        elif ftype == '_opgl':
            return 7

        return None



    def getKey(self, fname):

        result = fname[fname.find('_') : fname.rfind('_')]

        return result



    def getFiles(self):

        return self.fDic



    def getFileName(self, composifn):

        fname = composifn[0]
        fname = fname[fname.rfind('/') : ]

        return fname


    
    def setLogs(self, gname):

        logs = "Group: " + gname + " converted!"

        self.lb_logList.insert(END, logs)



    def getSize(self):

        return len(self.flist)