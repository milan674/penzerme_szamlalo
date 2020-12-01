import numpy as np
import cv2
from matplotlib import pyplot as plt

def Resize(img):            
    (h,w) = img.shape[:2]   
    print ("Az eredeti kep merete: ", (h,w)) 
    new_width=1024
    ratio = new_width /w  
    dim = (new_width,int(h * ratio) )
    resized = cv2.resize(img, dim, cv2.INTER_AREA) 
    print ("Az atmeretezett kep merete: ", resized.shape[:2] )
    return resized

def FindCircles(gray_img,radius): 
    circles = cv2.HoughCircles(gray_img,cv2.HOUGH_GRADIENT,1,180,param1=40,param2=10, minRadius=30, maxRadius=230)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        radius.append(i[2]) 
    print("     X    Y     R" )
    print(circles) 
    print(" Megtalaltam", circles.shape[1],  "db penzermet!")
    return circles

def averageIntensity(img, circles):
    av_values = []
    for coordinates in circles[0,:]:
        r=coordinates[2]
        coin= img[coordinates[1] - r:coordinates[1] + r, coordinates[0] - r:coordinates[0] + r] 
        coin_hls = cv2.cvtColor(coin, cv2.COLOR_RGB2HLS)
        avg_row = np.average(coin_hls, axis=0)
        avg_hls = np.average(avg_row, axis=0)
        av_values.append(np.around(avg_hls[0])) 
    print (av_values) 
    return av_values


def CoinAnalysis(radius,colour_values,Found_coins,output):  
    sum=0 
    count=0
    for i,j in zip (radius,colour_values):
        if j>=90:
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
        else:
                    print ("100 ft-os erme")
                    sum+=100
                    Found_coins.append(100)      

    for k in circles[0,:]:
         cv2.putText(output, str(Found_coins[count]),(k[0]-60,k[1]),cv2.FONT_HERSHEY_SIMPLEX, 3, (255,0,0), 5)
         count += 1
    cv2.putText(output,"Az ermek osszege: "+ str(sum)+ " Ft",(10,1300),cv2.FONT_HERSHEY_SIMPLEX, 2, (255,0,0),2)
    return sum

def DrawCircles(image,circles):  
    szamlalo = 1
    for i in circles[0, :]:
        cv2.circle(image, (i[0], i[1]), (i[2]), (0, 255, 0), 5) 
        #cv2.circle(image, (i[0], i[1]), 2, (255, 255, 0), 5) 
        #cv2.putText(image, str(szamlalo), ((i[0]) - 70, (i[1]) + 30), cv2.FONT_HERSHEY_SIMPLEX,1.5, (255, 0, 0),5) 
        szamlalo+=1
    return image


from tkinter import filedialog
import tkinter as tk


root = tk.Tk()
root.withdraw()
path = filedialog.askopenfilename()

img=cv2.imread(path) 
img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
resized=Resize(img) 
output=resized.copy() 

gray_img = cv2.cvtColor(resized.astype(np.uint8), cv2.COLOR_BGR2GRAY)   
blurred_img=cv2.GaussianBlur(gray_img,(27,27),0)


radius=[] 
circles=FindCircles(blurred_img,radius)  

Found_coins = [] 
colour_values = averageIntensity(output, circles)
sum=CoinAnalysis(radius,colour_values,Found_coins,output) 
output=DrawCircles(output,circles)  

plt.imshow(output) 
plt.show()
cv2.waitKey(0)
cv2.destroyAllWindows()
