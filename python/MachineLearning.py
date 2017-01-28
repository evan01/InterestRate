'''
This is a file that will train a ML network given a set of images.
'''
import os
from os import listdir
from os.path import isfile, join

import skimage
from skimage import io, color
from skimage.feature import hog
from sklearn import svm
from sklearn.externals import joblib
from tqdm import tqdm

size = (400, 400)
ImagesPath = "./python/trainingImages"


class SVM:
    svm = None
    instantiated = False

    def __init__(self):
        self.load()
        print "Instantiating the SVM"
        if self.svm == None:
            self.svm = svm.LinearSVC(verbose=4)
            self.instantiated = True

    def loadImages(self, test=False):

        avPath = "./python/trainingImages/AverageLooking"
        avImages = [f for f in listdir(avPath) if isfile(join(avPath, f))]

        gdPath = "./python/trainingImages/GoodLooking"
        gdImages = [f for f in listdir(gdPath) if isfile(join(gdPath, f))]

        if test:
            avImages, gdImages = avImages[:10], gdImages[:10]

        averageImages = []
        goodImages = []
        for img in tqdm(avImages, "Import Average Photos"):
            try:
                averageImages.append(skimage.transform.resize(color.rgb2grey(io.imread(avPath + "/" + img)), size))
            except:
                os.remove(avPath + "/" + img)
                continue

        for img in tqdm(gdImages, "Import Good Photos"):
            try:
                goodImages.append(skimage.transform.resize(color.rgb2grey(io.imread(gdPath + "/" + img)), size))
            except:
                os.remove(gdPath + "/" + img)
                continue
        return goodImages, averageImages

    def getFeatures(self, goodImages, avImages):
        data = []
        vals = []
        for good, av in tqdm(zip(goodImages, avImages), desc="Extract features"):
            try:
                fdGood, hog_image = hog(good, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1),
                                        visualise=True)
                fdAv, hog_image = hog(av, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)
            except:
                continue
            data.append(fdGood)
            vals.append("Good")
            data.append(fdAv)
            vals.append("Average")

        print "Done extracting features"
        return data, vals

    def train(self, data, values):
        '''
        This function will train the SVM network on it's data to learn to understand the expected values
        :param data:
        :return:
        '''
        self.svm.fit(data, values)

        print "Done training"

    def save(self):
        joblib.dump(self.svm, "./python/SVM_DATA.dat")

    def load(self):
        self.svm = joblib.load("./python/SVM_DATA.dat")

    def predict(self, data):
        '''
        This function will predict the SVM values of a whole lot of images
        :param data:
        :return:
        '''
        data = skimage.transform.resize(color.rgb2grey(data), size)
        fd, hog_image = hog(data, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(1, 1), visualise=True)
        return self.svm.predict(fd), self.svm.decision_function(fd)

def rate(img):
    s = SVM()
    prediction, decision = s.predict(img)


def main():
    s = SVM()
    goodImgs, avImgs = s.loadImages(test=False)
    imageData, imageVals = s.getFeatures(goodImgs, avImgs)
    s.train(imageData, imageVals)
    s.save()
    s = SVM()
    me = io.imread("/Users/eknox/workspace/InterestRate/python/trainingImages/IMG_1369.jpg")
    prediction, decision = s.predict(me)

    print "We are "+ str(100*decision[0])+"% sure that Evan is :  " + str(prediction[0])


if __name__ == '__main__':
    main()
