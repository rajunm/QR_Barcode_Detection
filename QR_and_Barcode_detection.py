#**********QR and Barcode detection using Pyzbar library**************

# Import necessary libraries
import numpy as np
import cv2
from pyzbar.pyzbar import decode                  # For decoding of QR and Barcode
import qrcode                                     # To generate custom QR Codes
import barcode                                    # To generate custom Barcode
from barcode import EAN13
from barcode.writer import ImageWriter

#+++++++++++++++++++++++++Generate a QR code+++++++++++++++++++++++++++++++++++
qr_code = qrcode.make("I am very bad")
qr_code.save('my_intro_qr.png')

           #-----------More control over the QRCode generation-------
controlled_qr_code = qrcode.QRCode(
    version=1,                                            # 1(smallest) to 40 --> indicates the size of QRCode
    error_correction= qrcode.constants.ERROR_CORRECT_M,   # controls the error correction used for the QR Code
                                                                # ERROR_CORRECT_L, ERROR_CORRECT_Q, ERROR_CORRECT_H
    box_size= 15,
    border=5
)
data = 'nothing is free'
controlled_qr_code.add_data(data)
controlled_qr_code.make(fit=True)
image = controlled_qr_code.make_image(fill_color='black', back_color='white')
#image.save("controlled_QR_generated.png")

#++++++++++++++++++++++++++++Barcode Generation+++++++++++++++++++++++++++++++++++

with open('barcode.png', 'wb') as f:
    EAN13('123456789102', writer=ImageWriter()).write(f)        # Accepts ONLY 12 digits. 13th digit is auto-generated

#+++++++++++++++++++Decode QRcode from an image++++++++++++++++++++++++++++++++++++

image = cv2.imread('barcode.png')   # eg:'controlled_QR_generated.png'
code = decode(image)
print(code)
cv2.namedWindow('image', flags=cv2.WINDOW_NORMAL)      # WINDOW_NORMAL or WINDOW_AUTOSIZE
cv2.imshow('image', image)
cv2.waitKey(0)
#image = cv2.imread('barcode.jpg')   # 'controlled_QR_generated.png'

#++++++++++++++++++++Decode multiple QR Codes in an image+++++++++++++++++++++++++++

#code = decode(image)
for decoded_code in code:
    print(decoded_code.data)
    my_data = decoded_code.data.decode('utf-8')       # Gives the actual data that was encoded
    print(my_data)
    points = np.array([decoded_code.polygon], np.int32)
    points = points.reshape((-1, 1, 2))
    cv2.polylines(image, [points], True, (255, 0, 255), 2)
    pts2 = decoded_code.rect
    cv2.putText(image, my_data, (pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,255),2)

cv2.imshow("Result", image)
cv2.waitKey(0)

#+++++++++++++++++++++Decode images captured from the camera+++++++++++++++++++++++++

def decode_camera_capture():
    camera = cv2.VideoCapture(0)
    camera.set(3,640)
    camera.set(4,480)
    while True:
        success, img = camera.read()
        for decoded_code in code:
            print(decoded_code.data)
            my_data = decoded_code.data.decode('utf-8')  # Gives the actual data that was encoded
            print(my_data)
            points = np.array([decoded_code.polygon], np.int32)
            points = points.reshape((-1,1,2))
            cv2.polylines(img, [points], True, (255,0,255), 5)
            pts2 = decoded_code.rect
            cv2.putText(image, my_data, (pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,255),2)

        cv2.imshow("Result", img)
        cv2.waitKey(1)
        if success == False:
            break
#decode_camera_capture()

cv2.destroyAllWindows()
