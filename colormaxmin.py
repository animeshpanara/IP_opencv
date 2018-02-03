import cv2
import sys
import numpy as np
import matplotlib.pyplot as plt 

p1=(0,0)
p2=(0,0)
mincol=[0,0,0]
maxcol=[0,0,0]

if(cv2.VideoCapture(1).isOpened()):
    video=cv2.VideoCapture(1)
else:
    video= cv2.VideoCapture(0)
if not video.isOpened():
        print ("Could not open video")
        sys.exit()
        
while True:
    
        # Read a new frame
        ok, frame = video.read()
        if not ok:
            break
        
        k = cv2.waitKey(1) & 0xff
        if k == 27 : break
        if k == 97 :
            bbox = cv2.selectROI(frame, False)
            print("BBOX:"+str(bbox))    
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))

            cropped=frame[p1[1]:p2[1],p1[0]:p2[0]]

            maxcol=[np.amax(cropped[:,:,0]),np.amax(cropped[:,:,1]),np.amax(cropped[:,:,2])]    
            mincol=[np.amin(cropped[:,:,0]),np.amin(cropped[:,:,1]),np.amin(cropped[:,:,2])]
            print("Max_Values:"+str(maxcol))
            print("Min_Values:"+str(mincol))
            
            color = ('b','g','r')
            hist_full = [cv2.calcHist([cropped],[0],None,[256],[0,256]),cv2.calcHist([cropped],[1],None,[256],[0,256]),cv2.calcHist([cropped],[2],None,[256],[0,256])]

            cv2.imshow("cropped",cropped)
            plt.subplot(221), plt.plot(hist_full[0],'b')
            plt.subplot(222), plt.plot(hist_full[1],'g')
            plt.subplot(223), plt.plot(hist_full[2],'r')
            plt.xlim([0,256])
            plt.show()
            #plt.waitforbuttonpress()
            #plt.close()
            #cv2.waitKey(0)
            cv2.destroyAllWindows()            
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)

        cv2.putText(frame,"MIN: "+str(mincol), (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0),2);
        cv2.putText(frame,"MAX: "+str(maxcol), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0,0,0),2);
        cv2.imshow("<------Camera------->", frame)
        
cv2.destroyAllWindows()
