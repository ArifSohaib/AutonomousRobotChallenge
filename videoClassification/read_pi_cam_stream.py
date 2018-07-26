import cv2
import numpy as np 
# from bs4 import BeautifulSoup
import urllib3

http = urllib3.PoolManager()

url = 'http://raspberrypi:8160/video'
print("connected")

while True:
    response = http.request('GET', url)
    print("got response")
    print(response.data)
    imgNp=np.array(bytearray(response.data), dtype=np.uint8)
    print(type(imgNp))
    print(imgNp.shape)
    img = cv2.imdecode(imgNp,-1)
    print(imgNp.shape)
    print("working")
    break
    # print(type(img))
    # cv2.imshow('test', img)
    # if cv2.waitKey(0) and 0xFF == ord('q'):
    #     cv2.destroyAllWindows()
    #     break