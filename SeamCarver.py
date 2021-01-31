import matplotlib.pyplot as plt
import numpy as np
import os
import sys

class SeamCarver:
    def __init__(self, img):
        self.img = img
        self.distTo = np.full(self.img.shape[0]*self.img.shape[1]+2, np.inf)
        self.edgeTo = np.full(self.img.shape[0]*self.img.shape[1]+2, 0)
        
    def energy_of_pixel(self, row, col):
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


    def showEnergyImg(self):
        energy_img = np.zeros((self.img.shape[0], self.img.shape[1]))
        for i in range(self.img.shape[0]):
            for j in range(self.img.shape[1]):
                energy_img[i][j] = self.energy_of_pixel(i, j)
        energy_img = energy_img/np.max(energy_img)*255
        plt.imshow(energy_img)
        plt.show()
            
    def serial(self, row, col):
        return row*self.img.shape[1] + col + 1
    def col(self, serial):
        return (serial-1)%self.img.shape[1]

if __name__ == '__main__':
    img = plt.imread('asdf.jpg')
    sc = SeamCarver(img)
    sc.showEnergyImg();
    
        
