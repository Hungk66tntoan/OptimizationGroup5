from PIL import Image
import cv2
import numpy as np
from clear_bad_boundary import ClearBadBoundary
from recognize_digit import RecognizeDigit
from cut_image_to_small_images import CutImageToSmallImages
from crop_white_corner import CropWhiteCorner
class ConvertImageToTxt:
    def __init__(self, image_path, txt_path, row, col):
        self.image_path = image_path
        self.txt_path = txt_path
        self.row = row
        self.col = col 
        self.data_array = np.zeros((self.row, self.col))
    
    def convert_to_numpy_array(self):
        self.raw_image = Image.open(self.image_path)
        self.gray_image = self.raw_image.convert('L')
        self.gray_np = np.array(self.gray_image)
    
    def crop_white_corner(self):
        cropper = CropWhiteCorner(self.gray_np)
        self.gray_np = cropper.crop()
    def cut(self):
        cutter = CutImageToSmallImages(self.gray_np, self.row, self.col)
        cutter.cut()
    def clear(self):
        for i in range(self.row):
            for j in range(self.col):
                clear = ClearBadBoundary(f'crop/crop_{i}_{j}.jpg')
                clear.clear()
                #crop white corner của cái crop/
                img = Image.open(f'crop/crop_{i}_{j}.jpg_clear.jpg').convert('L')
                img_np = np.array(img)
                cropper = CropWhiteCorner(img_np)
                after_crop = cropper.nice_crop()
                #lưu ảnh
                cv2.imwrite(f'crop/crop_{i}_{j}.jpg_clear.jpg', after_crop)
                
    def make_data_array(self):
        recognizer = RecognizeDigit()
        for i in range(self.row):
            for j in range(self.col):
                a = recognizer.recognize(f'crop/crop_{i}_{j}.jpg_clear.jpg')
                self.data_array[i][j] = a 
        #np.savetxt(self.txt_path, self.data_array, fmt='%d')
    def convert(self):
        self.convert_to_numpy_array()
        self.crop_white_corner()
        self.cut()
        self.clear()
        self.make_data_array()