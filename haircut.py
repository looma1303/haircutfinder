import cv2
import time
from PIL import Image
import pyautogui as pg
import requests
import json
import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QCoreApplication
global hairshop_name

class Start_window(QDialog):
    def __init__(self):
        super(Start_window, self).__init__()
        loadUi("start_window.ui", self)
        self.pushButton.clicked.connect(self.go_screen2)
        self.pushButton_2.clicked.connect(self.go_screen4)

    def go_screen4(self):
        screen3 = GetFile_Window_Other()
        wiget.addWidget(screen4)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_screen2(self):
        screen2 = Reservation_window()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()+1)


class Reservation_window(QDialog):
    def __init__(self):
        super(Reservation_window, self).__init__()
        loadUi("Reservation_window.ui", self)
        self.pushButton.clicked.connect(self.go_screen3)
        self.pushButton_2.clicked.connect(self.go_screen1)

    def go_screen3(self):
        screen3 = GetFile_Window()
        wiget.addWidget(screen3)
        widget.setCurrentIndex(widget.currentIndex()+1)

    def go_screen1(self):
        screen1 = Start_window()
        widget.addWidget(screen1)
        widget.setCurrentIndex(widget.currentIndex()-1)





class GetFile_Window(QDialog): #예약 O
    def __init__(self):
        super(GetFile_Window, self).__init__()
        loadUi("GetFile_Window.ui", self)
        self.pushButton.clicked.connect(self.File_find)
        #self.pushButton_2.clicked.connect(self.go_screen5)
        self.pushButton_3.clicked.connect(self.go_screen2)

    #def go_screen5(self):
        #만약 파일이 인식되지 않았다면 messagebox출력
        #파일이 인식됐다면 다음

    def go_screen2(self):
        screen2 = Reservation_window()
        widget.addWidget(screen2)
        widget.setCurrentIndex(widget.currentIndex()-1)

    def File_find(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText(fname[0])

class GetFile_Window_Other(QDialog):
    def __init__(self):
        super(GetFile_Window_Other, self).__init__()
        loadUi("GetFile_Window.ui", self)
        self.pushButton.clicked.connect(self.File_find)
        #self.pushButton_2.clicked.connect(self.go_screen5)
        self.pushButton_3.clicked.connect(self.go_screen1)

    #def go_screen5(self):
        #만약 파일이 인식되지 않았다면 messagebox출력
        #파일이 인식됐다면 다음

    def go_screen1(self):
        screen1 = Start_window()
        widget.addWidget(screen1)
        widget.setCurrentIndex(widget.currentIndex()-1)

    def File_find(self):
        fname = QFileDialog.getOpenFileName(self)
        self.label.setText(fname[0])











def find_face_eyes():
    cam = cv2.VideoCapture(0)
    cam.set(3,640)
    cam.set(4,480)
    ret, frame = cam.read()
    cv2.imwrite('001.jpg', frame)
    cam.release()
    cv2.destroyAllWindows()

    eyes_add = list()
    img_src = cv2.imread("001.jpg")
    img = cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)

    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
    eyeCascade = cv2.CascadeClassifier("haarcascade_eye.xml")
    face_data = faceCascade.detectMultiScale(img, scaleFactor=1.1, minNeighbors=1, minSize=(40,40))
    if len(face_data) > 0:

        face_recognize = True

        for f in face_data:

            x,y,w,h = f

            eyes = eyeCascade.detectMultiScale(img,1.1,3) #눈찾기
            if len(eyes) == 2:
                eye_recognize = True
                for e in eyes:
                    ex,ey,ew,eh = e
                    eyes_add.append([ex,ey,ew,eh])

                box_y = y - eyes_add[1][2]
                hairbox_1 = face_data[y:y+box_y, eyes_add[1][1]+eyes_add[1][3]]
                hairbox_2 = face_data[y:y+box_y, eyes_add[2][1]+eyes_add[2][3]]
                cv2.imwrite('hairbox_1.png',hairbox_1)
                cv2.imwrite('hairbox_2.png',hairbox_2)

            else:
                eye_recognize = False


            for e in eyes:
                ex,ey,ew,eh = e
                eyes_add.append([ex,ey,ew,eh])



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

    real_color = real_hair_color[0] + real_hair_color[1] + real_hair_color[2]
    box1_color = hair_color_1[0] + hair_color_1[1] + hair_color_1[2]
    box2_color = hair_color_2[0] + hair_color_2[1] + hair_color_2[2]
    gap = (real_color - box1_color) + (real_color - box2_color)
    if gap <= 100:
        print('something')

        #예약 ㄱ

    else:
        #아직 머리 짧
        print('something')



def get_reservaiton_information(residence):
    f = open('api_key.txt','r')
    line = f.readline()
    API_KEY = line
    api = GooglePlaces(line)
    places = api.search_place_by_coodinate()
    where = residence
    location = get_addr_place(where)
    radius = 100
    while len(places) == 1:
        places = api.search_places_by_coordinate(location, str(radius), 'beauty_salon')
        radius = radius -1
    place = places
    fields = ['name', 'formatted_address', 'international_phone_number', 'website']
    details = api.get_place_details(place['place_id'], fields)
    try:
        website = details['result']['website']
    except KeyError:
        website = ""

    try:
        name = details['result']['name']
    except KeyError:
        name = ""

    try:
        address = details['result']['formatted_address']
    except KeyError:
        address = ""

    try:
        phone_number = details['result']['international_phone_number']
    except KeyError:
        phone_number = ""

    try:
        reviews = details['result']['reviews']
    except KeyError:
        reviews = []

    #print('가장 가까운 미용실 이름:{name}'.format(name = name))
    rs = [website, name, address, phone_number, review]
    return rs
def asking_in_reservation(name,phone_number):

    dpdir = input("예약 하시곘습니까? y/n")
    if dpdir == 'y':
        reservation(name,phone_number)
    elif dpdir == 'n':
        print('처음 화면으로 돌아갑니다...')
        start()
    else:
        print('y 혹은 n을 입력해주세요')
        asking_in_reservation()
def reservation(name,phone_number):
    print('{name}의 전화번호는 {phone_number}입니다')
    bye = input('프로그램을 종료하시겠습니까? y/n')
    if bye == 'y':
        print('끝')
    elif bye == 'n':
        print('처음화면으로 돌아갑니다...')
        start()
    else:
        print('y 혹은 n을 입력해주세요')
        reservation(name,phone_number)
def asking():
    answer = input("당신의 머리가 긴편입니다. 가장 가까운 미용실을 예약할까요? y/n")
    if answer == 'y':
        get_reservaiton_information()
    elif answer == 'n':
        print("처음화면으로 돌아갑니다...")
        start_1()
    else:
        print("y나 n을 입력해주세요")
        asking()
class GooglePlaces(object):
    def __init__(self, API_KEY):
        super(GooglePlaces, self).__init__()
        self.apiKey = API_KEY

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
            }
        res = requests.get(endpoint_url, params = params)
        results = json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            time.sleep(2)
        return places
    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapi.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
            }
        res = requests.get(endpoint_url, params = params)
        place_details = json.loads(res.content)
        return place_details
def get_addr_place(location):

    url = 'http://maps.googleapis.com/maps/api/geocode/json?sensor=false&language=ko&addres={}'.format(location)

    response = requests.get(url)
    data = response.json()

    lat = data['results'][0]['geometry']['location']['lat']
    lng = data['results'][0]['geometry']['location']['lng']
    return  lat+','+lng

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = QtWidgets.QStackedWidget()
    screen1 = Start_window()
    screen2 = Reservation_window()
    screen3 = GetFile_Window()
    screen4 = GetFile_Window_Other()
    #screen5 =
    widget.addWidget(screen1)
    widget.addWidget(screen2)
    widget.addWidget(screen3)
    widget.addWidget(screen4)
    widget.setFixedHeight(300)
    widget.setFixedWidth(400)
    widget.show()
    app.exec_()
