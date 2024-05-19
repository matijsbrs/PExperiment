# First, install the necessary libraries if you haven't already:
# pip install pyzbar
# pip install opencv-python

import cv2
from pyzbar import pyzbar

def find_barcode(image_path, output_path='barcode.jpg'):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Find barcodes in the image
    barcodes = pyzbar.decode(gray)

    for barcode in barcodes:
        # Extract the bounding box location of the barcode and draw a rectangle around it
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        
        # The barcode data is a bytes object so if we want to draw it on our output image
        # we need to convert it to a string first
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        
        # Draw the barcode data and barcode type on the image
        text = f"{barcode_data} ({barcode_type})"
        print(f"found code: {barcode_data} ({barcode_type})")
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    
    # Find qrcodes in the image
    qrcodes = pyzbar.decode(gray, symbols=[pyzbar.ZBarSymbol.QRCODE])
    
    for qrcode in qrcodes:
        # Extract the bounding box location of the qrcode and draw a rectangle around it
        (x, y, w, h) = qrcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # The qrcode data is a bytes object so if we want to draw it on our output image
        # we need to convert it to a string first
        qrcode_data = qrcode.data.decode('utf-8')
        qrcode_type = qrcode.type
        
        # Draw the qrcode data and qrcode type on the image
        text = f"{qrcode_data} ({qrcode_type})"
        print(f"found code: {qrcode_data} ({qrcode_type})")

        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    # Show the output image
    # cv2.imshow("Barcode Detection", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Save the output image with detected barcodes
    cv2.imwrite(output_path, image)

# Replace 'path_to_image.jpg' with your image path
find_barcode('1624.5.jpg')
