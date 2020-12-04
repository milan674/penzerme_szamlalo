import numpy as np
import cv2
from matplotlib import pyplot as plt
from tkinter import filedialog
import tkinter as tk

#1.rész: kép átméretezés, szürkeárnyalatossá alakítás,Gauss szűrő alkalmazása, körök megkeresése a képen
def Resize(img):            # kép átméretezése
    (h,w) = img.shape[:2]   #eredeti kép magasságának és szélességének lekérdezése
    print ("Az eredeti kep merete: ", (h,w)) 
    new_width=1024 # megadom, hogy mekkora legyen az új szélesseg :  Ebből kiszámolja  a magasságot, így az arányok nem változnak
    ratio = new_width /w  # az új és régi szélesseg aránya ---> ezzel kell beszorozni a régi magasságot, es megkapom az új magasságot
    dim = (new_width,int(h * ratio) ) # új magasság, új méret kiszámítása     dim -> tuple = (uj_szelesseg,uj_magassag)
    resized = cv2.resize(img, dim, cv2.INTER_AREA)  # átméretezés
    print ("Az atmeretezett kep merete: ", resized.shape[:2] )
    return resized

def FindCircles(gray_img,radius): #körök megkeresése : HoughCircles segítségével
    circles = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,180,param1=40,param2=10, minRadius=30, maxRadius=230)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        radius.append(i[2]) # a körök sugarait tároló tömbhöz hozzáfűzi az aktuális kör sugarának az értékét
    print("     X    Y     R" )
    print(circles) # megtalált körök középpontjának x és y koordinátái, és sugara
    print(" Megtalaltam", circles.shape[1],  "db penzermet!")
    return circles

# 2. rész: megtalált körök elemzése: milyen intenzitású, mekkora a sugara?--> milyen érme? 
def averageIntensity(img, circles):
    av_values = []
    for coordinates in circles[0,:]:
        r=coordinates[2]
        coin= img[coordinates[1] - r:coordinates[1] + r, coordinates[0] - r:coordinates[0] + r] 
        coin_hls = cv2.cvtColor(coin, cv2.COLOR_RGB2HLS) # másik színrendszer használata
        avg_row = np.average(coin_hls, axis=0)
        avg_hls = np.average(avg_row, axis=0)
        av_values.append(np.around(avg_hls[0]))  # hue = avg_hls[0]
    print (av_values) 
    return av_values


def CoinAnalysis(radius,colour_values,Found_coins,output):  # melyik körben milyen típusú érme van?
    sum=0 #pénzérmék összegét tárolja
    count=0
    for i,j in zip (radius,colour_values):
        if j>=90 and j<=130:
            if i>80 and i<115:
                 print ("10 ft-os erme")
                 sum+=10
                 Found_coins.append(10)
            else:
                print ("50 ft-os erme")
                sum+=50
                Found_coins.append(50)
        elif j<78:
            if i<104:
                 print("5 Ft-os erme")
                 sum+=5
                 Found_coins.append(5)
            elif i>120 and j>=60:
                 print ("200 ft-os erme")
                 sum+=200
                 Found_coins.append(200)
            elif (i>=104 and j<60):
                 print ("20 ft-os erme")
                 sum+=20
                 Found_coins.append(20)
        elif j<90 and j>=78:
                 print ("100 ft-os erme")
                 sum+=100
                 Found_coins.append(100)      
        else:
                 print("egyeb targy")
                 Found_coins.append(0)

    for k in circles[0,:]:  #pénzérmék típusainak kiirása a képre
         cv2.putText(output, str(Found_coins[count]),(k[0]-60,k[1]),cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5)
         count += 1
    cv2.putText(output,"Az ermek osszege: "+ str(sum)+ " Ft",(10,100),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0),2)
    return sum

def DrawCircles(image,circles):   # megtalált körök megrajzolása és kiírja a képre, hogy melyik érmét hányadiknak tárolta el
    szamlalo = 1
    for i in circles[0, :]:
        cv2.circle(image, (i[0], i[1]), (i[2]), (0, 255, 0), 5) # rajzol egy kört az érmék köré
        #cv2.circle(image, (i[0], i[1]), 2, (255, 255, 0), 5) # megrajozlja a kör középpontját
        # kiírja a képre, hogy melyik érmét hányadik helyen találta
        cv2.putText(image, str(szamlalo), ((i[0]) - 70, (i[1]) + 30), cv2.FONT_HERSHEY_SIMPLEX,1.5, (255, 0, 0),5) 
        szamlalo+=1
    return image

#-------------MAIN----------
#1.rész: kép átméretezés, szürkeárnyalatossá alakítás,Gauss szűrő alkalmazása, körök megkeresése a képen
#img = cv2.imread('test/545.jpg') # kép beolvasása

root = tk.Tk()
root.withdraw()
path = filedialog.askopenfilename()
print(path)

img=cv2.imread(path) 

img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
resized=Resize(img)  #kép átméretezése
output=resized.copy()  # Másolat az átméretezett színes képről, később erre írom ki a találatokat

gray_img = cv2.cvtColor(resized.astype(np.uint8), cv2.COLOR_BGR2GRAY)   #szürkeárnyalatossá alakítás
blurred_img=cv2.GaussianBlur(gray_img,(27,27),0)# Gauss szűrő alkalmazása, a részleteket elrejti, azokra a körök keresésénel nincs szükség

radius=[]  # ebben tárolom el a körök sugarát
circles=FindCircles(blurred_img,radius)  # körök megkeresése, kör középpontjának x,y koordinátáinak eltárolása, kör sugarának eltárolása

# 2. rész: megtalált körök elemzése: milyen intenzitású, mekkora a sugara?--> milyen érme?   kimeneti kép elkészítése
Found_coins = []   # ebben tárolja el, hogy milyen értékű érméket talált
colour_values = averageIntensity(output, circles)   # talált körök (érmék) átlagos színintenzitások eltárolása
sum=CoinAnalysis(radius,colour_values,Found_coins,output) # Eldönti, hogy a talált érmék milyen típusúak és mennyi az összértékük ->sum , kiiras a képre
output=DrawCircles(output,circles)  #a kimeneti képen megrajzolja a megtalált köröket

plt.imshow(output) 
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
