import cv2
import time
from PIL import Image
import pyautogui as pg
import requests
import json
import sys
from PyQt5.QtWidgets import  QApplication, QWidget, QPushButton, QMessageBox
from PyQt5.QtCore import QCoreApplication
class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        place_yes_btn = QPushButton('예',self)
        place_yes_btn.resize(yes_btn.sizeHint())

        place_no_btn = QPushButton('아니오',self)
        place_no_btn.resize(no_btn.sizeHint())
        place_no_btn.move(20,30)

        self.setGeometry(300,300,300,300)
        self.setWindowTitle('hairshop finder')

        place_yes_btn.clicked.connect(self.place_buttonClicked)
        place_no_btn.clicked.connect(self.place_buttonClicked)
        self.show()


    def place_buttonClicked(self):
        sender = self.sender()
        if sender.text() == '예':
            #거주지를 입력해주세요 (get_reservaiton_information)
        elif sender.text() == '아니오':
            #미용실 예약기능을 사용하지 않으시겠습니까 messagebox
        else:
            pass
            



    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit?',
                                     '종료하시겠습니까?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if not type(event) == bool:
                event.accept()
            else:
                sys.exit()
        else:
            if not type(event) == bool:
                event.ignore()


'''
def start():
    off =input("당신의 머리길이를 측정하고 미용실을 예약해주는 프로그램입니다. y:계속, n:프로그램 종료")
    if off == 'y':
        find_face_eyes()
    elif off == 'n':
        print("프로그램을 종료합니다..")
    else:
        print("y 혹은 n을 입력해주세요.")
        start()
def reservation_start():
    aldydtlf = input("가장 가까운 미용실을 예약하기 위해 거주지를 알려주시겠습니까? y/n")
    if aldydtlf == 'y':
        get_reservaiton_information()
    elif aldydtlf == 'n':
        start_1()
    else:
        print("y 혹은 n을 입력해주세요.")
        reservation_start()
def start_1():

    dksgo = input("미용실 예약기능을 사용하지 않으시겠습니까? y(사용하지 않는다)/n(사용한다.)")
    if dksgo == 'y':
        print("처음화면으로 넘어갑니다...")
        start()


    elif dksgo == 'n':
        print("다음단계로 넘어갑니다...")
        get_reservaiton_information()


    else:
        print("y 혹은 n을 입력해주세요")
        start_1()
'''
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

        print("얼굴인식 완료")

        for f in face_data:

            x,y,w,h = f

            eyes = eyeCascade.detectMultiScale(img,1.1,3) #눈찾기
            for e in eyes:
                ex,ey,ew,eh = e
                eyes_add.append([ex,ey,ew,eh])


    else:
        print("얼굴이 인식되지 않았습니다.\n")

    box_y = y - eyes_add[1][2]
    hairbox_1 = face_data[y:y+box_y, eyes_add[1][1]+eyes_add[1][3]]
    hairbox_2 = face_data[y:y+box_y, eyes_add[2][1]+eyes_add[2][3]]
    cv2.imwrite('hairbox_1.png',hairbox_1)
    cv2.imwrite('hairbox_2.png',hairbox_2)

    hairbox_scan()
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

        asking()

    else:
        print("아직 머리 짧음")
        print("처음 화면으로 돌아갑니다...")
        start()




def get_reservaiton_information():
    f = open('api_key.txt','r')
    line = f.readline()
    API_KEY = line
    api = GooglePlaces(line)
    places = api.search_place_by_coodinate()
    where = input('거주지를 입력해주세요: ex)순천시 매곡동 매산고등학교')
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

    print('가장 가까운 미용실 이름:{name}'.format(name = name))

    asking_in_reservation(name,phone_number)
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
    w = GUI()
    sys.exit(app.exec_())
