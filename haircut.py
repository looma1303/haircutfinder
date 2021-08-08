import numpy as np
import cv2
from urllib.parse import quote_plus
from bs4 import BeautifulSoup
from selenium import webdriver
import time
from PIL import Image
import pyautogui as pg
import pyautogui as pag
from PIL import ImageGrab
import googlemaps
import pprint
from GoogleMapsAPIKey import get_my_key

def start():
    off =input("당신의 머리길이를 측정하고 미용실을 예약해주는 프로그램입니다. y:계속, n:프로그램 종료")
    if off == 'y':
        start_()
    elif off == 'n':
        print("프로그램을 종료합니다..")
    
def start_():
    aldydtlf = input("가장 가까운 미용실을 예약하기 위해 거주지를 알려주시겠습니까? y/n")
    if aldydtlf == 'y':
        get_reservation_information()
    elif aldydtlf == 'n':
        start_1()
    else:
        print("y 혹은 n을 입력해주세요.")
        start_()
        
        
            
def start_1():
    
    dksgo = input("미용실 예약기능은 사용할수 없습니다 괜찮으시겠습니까?")
    if dksgo == 'y':
        
        print("다음 단계로 넘어갑니다...")
        find_face_eyes()
            
    elif dksgo == 'n':
        print("처음화면으로 넘어갑니다...")
        start()

        
    else:
        print("y 혹은 n을 입력해주세요")
        start_1()
    
def find_face_eyes():
    
    eyes_add = list()
    img_src = cv2.imread("001.jpg")
    img = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)
    img2 = img_src
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    face_data = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=1, minSize=(40,40))
    if len(face_data) > 0:
        
        print("얼굴인식 완료")
        color = (0,0,255)
        for f in face_data:
            
            x,y,w,h = f
            eye_pic = face_data[y:y+h:,x:x+w]
            eyes = eyeCascade.detectMultiScale(img,1.1,3) #눈찾기
            for e in eyes:
                ex,ey,ew,eh = e
                eyes_add.append([ex,ey,ew,eh])
        face_add = [x,y,w,h]
    
    else: 
        print("얼굴이 인식되지 않았습니다.\n")
    
    box_y = y - eyes_add[1][2]
    hairbox_1 = face_data[y:y+box_y, eyes_add[1][1]+eyes_add[1][3]]
    hairbox_2 = face_data[y:y+box_y, eyes_add[2][1]+eyes_add[2][3]]
    cv2.imwrite('hairbox_1.png',hairbox_1)
    cv2.imwrite('hairbox_2.png',hairbox_2)


def hairbox_scan():
    hairbox1 = Image.open('hairbox_1.png')
    hairbox2 = Image.open('hairbox_2.png')
    hairfull_img = Image.open('hairfull_img.jpg')
    point_1 = pg.center(hairbox1)
    point_2 = pg.center(hairbox2)
    point_hair_color = pg.center(hairfull_img)
    hair_color_1 = hairbox1.getpixel(point_1)
    hair_color_2 = hairbox2.getpixel(point_2)
    real_hair_color = hairfull_img.getpixel(point_hair_color)
    
    if real_hair_color == hair_color_1 or real_hair_color == hair_color_2:
        asking()
        
    else:
        print("아직 머리 짧음")
        print("처음 화면으로 돌아갑니다...")
        start()
    
    
def get_reservation_information():
    f = open('api_key.txt','r')
    line = f.readline()
    API_KEY = line
    
    



def asking():
    answer = input("당신의 머리가 긴편입니다. 가장 가까운 미용실을 예약할까요? y/n")
    if answer == y:
        reservation()
    elif answer == n:
        print("처음화면으로 돌아갑니다...")
        start()
    else:
        print("y나 n을 입력해주세요")
        asking()
        
def reservation():
    
