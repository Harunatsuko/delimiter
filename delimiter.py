import pygame
import numpy as np
import os
from pygame import *
import cv2

WIN_WIDTH = 700 
WIN_HEIGHT = 700
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)
BACKGROUND_COLOR = (255,0,0)

class Delimiter():
    '''
    Part of preprocessing image pipeline
    Parameters
    ----------
    path_to_dataset : str, required
        Path to folder - dataset with source, raw scraped images
    path_to_save : str, required
        Path to folder where to save part of images
    name_prefix : str, optional
        Prefix for the filenames of images parts, should be changed each run
        if path_to_save is the same as previous run
    '''
    def __init__(self, path_to_dataset, path_to_save, name_prefix='cut_'):
        self.name_prefix = name_prefix + '_'
        self.path_to_dataset = path_to_dataset
        self.path_to_save = path_to_save
        self.img_num = 0
        self.process_state = False
        self.init_images_path()
        self.curr_img_id = 0
        pygame.init()

        screen = pygame.display.set_mode(DISPLAY,pygame.RESIZABLE)
        pygame.display.set_caption("Delimiter")

        # set the first image
        self.curr_img = self.resize_img(cv2.rotate(cv2.cvtColor(cv2.imread(self.imgs_path[self.curr_img_id]),
                                                cv2.COLOR_BGR2RGB),
                                    cv2.ROTATE_90_COUNTERCLOCKWISE))
        tmp_mask = np.ones((WIN_WIDTH,WIN_HEIGHT,3),np.uint8)
        tmp_mask[0:self.curr_img.shape[0], 0:self.curr_img.shape[1], :] = self.curr_img
        self.curr_img = tmp_mask

        self.bg = Surface(DISPLAY)
        pygame.surfarray.blit_array(self.bg, self.curr_img)
        screen.blit(self.bg, (0,0))
        self.screen = screen

    def resize_img(self, img):
        '''
        Resize image to the display size
        keeping proportions
        '''
        if img.shape[0] > img.shape[1]:
            diff = img.shape[1] / img.shape[0]
            img_shape_0 = WIN_WIDTH
            img_shape_1 = np.int0(img_shape_0 * diff)
            img = cv2.resize(img, (img_shape_1, img_shape_0))
        else:
            diff = img.shape[0] / img.shape[1]
            img_shape_1 = WIN_WIDTH
            img_shape_0 = np.int0(img_shape_1 * diff)
            img = cv2.resize(img, (img_shape_1, img_shape_0))
        return img

    def init_images_path(self):
        imgs_path = []
        for root, _, files in os.walk(os.path.abspath(self.path_to_dataset), topdown = False):
            for f in files:    
                img_name = os.path.join(root,f)
                imgs_path.append(img_name)
        self.imgs_path = imgs_path

    def update(self):
        pygame.surfarray.blit_array(self.bg, self.curr_img)
        if self.process_state:
            self.draw_process_rect()
        self.screen.blit(self.bg, (0,0))

    def draw_process_rect(self):
        '''
        Draw rect while cutting part of image
        '''
        curr_x, curr_y = pygame.mouse.get_pos()
        w = np.abs(self.start_pos[0] - curr_x)
        h = np.abs(self.start_pos[1] - curr_y)
        pygame.draw.rect(self.bg, (255,0,0), (self.start_pos[0], self.start_pos[1], w,h), 2)

    def handle_left_mbt(self, pos, type):
        x,y = pos
        if type == 'down':
            self.start_pos = pos
            self.process_state = True
        else:
            self.process_state = False
            self.save_img_part(pos)
    
    def save_img_part(self, end_pos):
        xs, ys = self.start_pos
        xe, ye = end_pos
        img = self.curr_img[xs:xe, ys:ye].copy()
        img = cv2.rotate(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cv2.ROTATE_90_CLOCKWISE)
        self.img_num = self.img_num + 1
        img_path = os.path.join(self.path_to_save, self.name_prefix+str(self.img_num)+'.jpg')
        cv2.imwrite(img_path, img)
    
    def next_image(self):
        self.curr_img_id = self.curr_img_id + 1
        self.curr_img = self.resize_img(cv2.rotate(cv2.cvtColor(cv2.imread(self.imgs_path[self.curr_img_id]),
                                                cv2.COLOR_BGR2RGB),
                                    cv2.ROTATE_90_COUNTERCLOCKWISE))
        tmp_mask = np.ones((WIN_WIDTH,WIN_HEIGHT,3),np.uint8)
        tmp_mask[0:self.curr_img.shape[0], 0:self.curr_img.shape[1], :] = self.curr_img
        self.curr_img = tmp_mask

    def delete_img(self):
        os.remove(self.imgs_path[self.curr_img_id])