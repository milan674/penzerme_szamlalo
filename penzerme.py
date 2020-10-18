import numpy as np
import cv2
from matplotlib import pyplot as plt

# kep beolvasasa
img = cv2.imread('1.jpg')

# kep atmeretezese
(h, w) = img.shape[:2]   # eredeti kep magassaganak es szelessegenek lekerdezese 
print ("Az eredeti kep merete: ", (h,w)) 
new_width=800  # megadom, hogy mekkora legyen az uj szelesseg :  Ebbol kiszamolja  a magassagot, igy az aranyok nem valtoznak
ratio = new_width /w  # az uj es regi szelesseg aranya ---> ezzel kell beszorozni a regi magassagot, es megkapom az uj magassagot
dim = (new_width,int(h * ratio) ) # uj magassag, uj meret kiszamitasa     dim -> tuple = (uj_szelesseg,uj_magassag)
resized = cv2.resize(img, dim, cv2.INTER_AREA)  # atmeretezes
print ("Az atmeretezett kep merete: ", dim )

output=resized.copy()  # Masolat az atmeretezett szines keprol, kesobb erre irom ki a talalatokat

#szurkearnyalatossa alakitas
gray_img = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY) 
# Gauss szűrő alkalmazasa, a reszleteket elrejti
gray_img= cv2.GaussianBlur(gray_img,(11,11),cv2.BORDER_DEFAULT)

cv2.imshow("g",gray_img)

#KOROK MEGKERESESE : HoughCircles fgv 
korok = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,120,param1=40,param2=35, minRadius=50, maxRadius=200)
print(korok) # megtalalt korok x,y koord és r sugar
#print(korok.shape) # a masodik tagja az, hogy mennyi kort talalt
print(" Megtalaltam", korok.shape[1],  "db penzermet!")

# megtalalt korok megrajzolasa,  es egyelore kiirja a kepre, hogy melyik ermet hanyadiknak tarolta el a tombben
szamlalo = 1
for i in korok[0, :]:
    cv2.circle(output, (i[0], i[1]), int(i[2]), (0, 255, 0), 5) # rajzol egy kort az ermek kore
    cv2.circle(output, (i[0], i[1]), 2, (255, 255, 0), 5) # megrajozlja a kor kozeppontjat
    cv2.putText(output, str(szamlalo), (int(i[0]) - 70, int(i[1]) + 30), cv2.FONT_HERSHEY_SIMPLEX, 3, (255, 0, 0),5) # kiirja a kepre, hogy melyik ermet hanyadik helyen talalta
    szamlalo+=1
 
# 2. resz: megtalalt korok elemzese: milyen intenzitasu, mekkora a sugara--> milyen erme? 



plt.imshow(output, cmap="gray")  # megjelenites szurkearnyalatosan
plt.colorbar()  # intenzitas mutato
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
