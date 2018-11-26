import cv2
import imutils
 
'''
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Camninho para imagem")
args = vars(ap.parse_args())
'''

#----------------------------#
lower = (120,50,180)
upper = (210,150,240)


#image = cv2.imread(args["image"])
ori = cv2.imread('./images/2.bmp')

cv2.imshow("Original", ori)
cv2.imwrite('./ori.jpg', ori)

gray = cv2.cvtColor(ori, cv2.COLOR_BGR2GRAY)
#image = imutils.resize(ori, width=600)

image = gray


cv2.imshow("Gray", image)

# desfocagem
blurred = cv2.GaussianBlur(image, (13,13), 0)
cv2.imshow("blurred", blurred)

#threshold = cv2.THRESH_TRUNC
threshold = cv2.THRESH_TOZERO
#threshold = cv2.THRESH_TOZERO_INV
#threshold = cv2.THRESH_BINARY

edged = cv2.threshold(blurred, 160, 255, threshold)[1]
#edged = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 5)


cv2.imshow('threshold GaussianBlur', edged )
cv2.waitKey(0)

#erode = cv2.dilate(blurred.copy(), None, iterations=3)

i_dilate = 20
i_erode = 25

contorno = False


while contorno == False:

    erode = cv2.dilate(blurred.copy(), None, iterations=i_dilate)
    dila = cv2.erode(erode.copy(), None, iterations=i_erode)
    edged1 = cv2.threshold(dila, 165, 255, threshold)[1]

    cv2.imshow("erode", erode)
    cv2.imshow("dila ", dila)
    cv2.imshow("threshold dila erode", edged1)
    cv2.imwrite('./transf.jpg', edged1)
    cv2.waitKey(0)





    edged1= cv2.Canny(edged1,0 ,255)

    #cv2.imshow("Original", image)

    #----------------------#
     
    #(_, cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    (_, cnts0, _) = cv2.findContours(edged1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cnts = sorted(cnts0, key = cv2.contourArea, reverse = True)[:1]
    rect = None

    #hull = [cv2.convexHull(c) for c in cnts]

    if len(cnts) > 0:
        for c in cnts:
                # Encontramos o maior contorno na máscara, e então usamos para calcular o círculo mínimo de fechamento e centro do centróide
                '''
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                (cX, cY) = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

                # Basta desenhar o círculo delimitador e texto, se o raio atende um tamanho mínimo
                if radius > 5:
                    cv2.circle(ori, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                '''
                x, y, w, h = cv2.boundingRect(c)
                L = 20
                LL = L * 2 
                xx, yy, ww, hh = x-L, y-L, w+LL, h+LL
                # draw a green rectangle to visualize the bounding rect
                cv2.rectangle(ori, (x, y), (x+w, y+h), (0, 255, 0), 2)
                cv2.rectangle(ori, (xx, yy), (xx+ww, yy+hh), (255, 0, 0), 2)

                contorno = True


    else:
        contorno = False
        i_erode -= 3
        i_dilate -= 3





clone = ori.copy()


cv2.drawContours(clone, cnts, -1, (0, 255, 255), 2)
#cv2.drawContours(clone, hull, -1, (255, 0, 0), 2)
try:
    cv2.drawContours(clone, [rect], -1, (0, 0, 255), 2)
except:
    pass 

#cv2.imshow("Blurred", blurred)
#cv2.imshow("Canny", contor)
cv2.imshow("Contornos", clone)

cv2.imwrite('./Box.jpg', clone)





cv2.waitKey(0)