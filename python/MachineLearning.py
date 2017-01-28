'''
This is a file that will train a ML network given a set of images.
'''
from sklearn import svm

ImagesPath = "./python/trainingImages"
class SVM:
    svm = None

    def __init__(self):
        print "Instantiating the SVM"
        self.svm = svm.LinearSVC()

    def loadImages(self):


    def train(self,data,values):
        '''
        This function will train the SVM network on it's data to learn to understand the expected values
        :param data:
        :return:
        '''
