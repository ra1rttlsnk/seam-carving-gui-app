import matplotlib.pyplot as plt
import numpy as np
import os
import sys

class SeamCarver:
    
    def __init__(self, img):
        self.img = img
        self.distTo = np.full(self.img.shape[0]*self.img.shape[1]+2, np.inf)
        self.edgeTo = np.full(self.img.shape[0]*self.img.shape[1]+2, 0)
        self.energies = np.zeros((img.shape[0], img.shape[1]))
        self.calculateEnergies()
        
    def energyOfPixel(self, row, col):
        if row == 0 or row == self.img.shape[0]-1 or col == 0 or col == self.img.shape[1]-1:
                return 1000
        if len(img.shape) == 2:
            en = ((self.img[row+1][col] - self.img[row-1][col])**2 +
            (self.img[row][col+1] - self.img[row][col-1])**2)
            return np.sqrt(en)
        elif len(self.img.shape) == 3:
            en = ((self.img[row+1, col, :] - self.img[row-1, col, :])**2 +
            (self.img[row,col+1,:] - self.img[row,col-1,:])**2)
            return np.sum(en)
        else:
            return 0

    def calculateEnergies(self):
        for i in range(self.img.shape[0]):
            for j in range(self.img.shape[1]):
                self.energies[i][j] = self.energyOfPixel(i, j)

    def showEnergyImg(self):
        self.energies = energy_img/np.max(energy_img)*255
        plt.imshow(self.energies)
        plt.show()

    def serial(self, row, col):
        return row*self.img.shape[1] + col + 1
    def col(self, serial):
        return (serial-1)%self.img.shape[1]
    def row(self, serial):
        return (serial-1)//self.img.shape[1]

    def relaxEdge(self, a, b):
        d = self.distTo[a]+ self.energies[self.row(b), self.col(b)]
        if d < self.distTo[b]:
            self.edgeTo[b] = a
            self.distTo[b] = d
    def relaxTarget(self, a, b):
        d = self.distTo[a]
        if d < self.distTo[b]:
            self.edgeTo[b] = a
            self.distTo[b] = d
    def relaxThree(self, a):
        r = self.row(a)
        c = self.col(a)
        if c-1 >=0 and r < self.img.shape[0]-1:
            self.relaxEdge(a, self.serial(r+1,c-1))
        if c+1 < self.img.shape[1] and r < self.img.shape[0] - 1:
            self.relaxEdge(a, self.serial(r+1,c+1))
        if r < self.img.shape[0] - 1:
            self.relaxEdge(a, self.serial(r+1, c))
    def relax(self):
        self.distTo[0] = 0
        for i in range(1, self.img.shape[1]+1):
            self.distTo[i] = self.energyOfPixel(0, i - 1)
        for i in range(self.img.shape[0]-1):
            for j in range(self.img.shape[1]):
                self.relaxThree(self.serial(i, j))
        for i in range(self.img.shape[1]):
            self.relaxTarget(self.serial(self.img.shape[0]-1, i), len(self.distTo)-1)


    def findSeam(self):
        self.relax()
        xIndices = []
        s = self.edgeTo[len(self.edgeTo)-1]
        while(s != 0):
            xIndices.append(self.col(s))
            s = self.edgeTo[s]
        return xIndices
    
    def removeSeam(self):
        xIndices = self.findSeam()
        resized_img = np.zeros((self.img.shape[0], self.img.shape[1]-1, 3), dtype='uint8')
        resized_energies = np.zeros((self.img.shape[0], self.img.shape[1]-1), dtype='uint8')
        
        for i in range(self.img.shape[0]):
            xIndex = xIndices[self.img.shape[0]-1-i]
            resized_img[i,:xIndex,:] = self.img[i,:xIndex,:]
            resized_energies[i,:xIndex] = self.energies[i,:xIndex]
            resized_img[i,xIndex:,:] = self.img[i,xIndex+1:,:]
            resized_energies[i,xIndex:] = self.energies[i,xIndex+1:]
            
        self.img = resized_img
        self.energies = resized_energies
        self.distTo = np.full(self.img.shape[0]*self.img.shape[1]+2, np.inf)
        self.edgeTo = np.full(self.img.shape[0]*self.img.shape[1]+2, 0)
        self.recalculateEnergyAlongSeam(xIndices)
        
    def recalculateEnergyAlongSeam(self,xIndices):
        for i in range(self.energies.shape[0]):
            self.energies[i, xIndices[self.energies.shape[0]-i-1]] = self.energyOfPixel(i, xIndices[self.energies.shape[0]-i-1]) 
    def showImage(self):
        plt.imshow(self.img/255)
        plt.show()

    
    

if __name__ == '__main__':
    import time
    img = plt.imread('asdf.jpg')
    sc = SeamCarver(img)
    a = time.time()
    for i in range(2):
        sc.removeSeam()
    sc.showImage()
    plt.imsave('asdf2.jpg', sc.img)
    print("Elapsed time: {}".format((time.time()-a)/60))
    
        
