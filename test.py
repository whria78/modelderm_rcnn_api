###
### Model Dermatology RCNN (http://rcnn1.modelderm.com) REST API
### Han Seung Seog (whria78@gmail.com) 
### 
### 2020-8-8
###
 
 
display_status=False 
import os
img_root=os.path.join(os.getcwd(),'examples')
dest_root=os.path.join(os.getcwd(),'RESULT')

import requests
import sys
import random
import string
import cv2   
import numpy as np
import threading
import time
 
# for python2 python3 compatibility
try:
    import urllib.parse as myurl
except ImportError:
    import urllib as myurl
from io import BytesIO


def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join((random.choice(letters_and_digits) for i in range(length)))
 
# for unicode support
def custom_filename(x):return myurl.quote(x)
 
def get_server_status(url,unique_id):
    result_=requests.get('%s?%s' % (url,unique_id))
    if result_.status_code!=200:
        print (result_.status_code)
        sys.exit(1)
    return result_.text.split(',') #currentusers_,message_

stop_thread=False
def show_status(unique_id):
    global stop_thread
    time.sleep(3)
    while stop_thread==False:
        currentusers_,message_=get_server_status(server_url,unique_id)
        print(message_)
        time.sleep(1)

def modelderm(url,unique_id,image_path):
    args1_=unique_id
    args2_=''
    
    file_={'file':(custom_filename(os.path.basename(image_path)),open(image_path,'rb').read(),'Content-Type:image')}
    data_={'args1':args1_,'args2':args2_}

    if display_status:
        stop_thread=False
        th_=threading.Thread(target=show_status,args=(unique_id,))
        th_.daemon=True
        th_.start()
 
    res=requests.post(url,files=file_,data=data_)

    if display_status:
        stop_thread=True
    return res.content

### Server List ### 
server_url='https://rcnn1.modelderm.com/magi2'


###
### GENERATE UNIQUE ID FOR CHECKING STATUS
###
unique_id=get_random_alphanumeric_string(8)


###
### GET SERVER STATUS
###
currentusers_,message_=get_server_status(server_url,unique_id)
print("Current users : %s" % (currentusers_))
print(message_)


###
### PREPARE IMAGE LIST
###

if len(sys.argv)>1:     img_root=str(sys.argv[1])
if len(sys.argv)>2:     dest_root=str(sys.argv[2])

img_root=os.path.abspath(img_root)
   
img_list=[]
if os.path.isdir(img_root):
    for root,dirs,files in os.walk(img_root):
        for fname in files:
            ext=(os.path.splitext(fname)[-1]).lower()
            if ext == ".jpg" or ext == ".jpeg" or ext == ".png" or ext == ".webp": 
                img_path=os.path.join(root,fname)
                img_list+=[img_path]
else:
    img_list=[img_root]
    img_root=os.path.dirname(img_list[0])

print("### Source folder  : ",img_root)
print("### Destination folder : ",dest_root)
f_result=open(os.path.join(dest_root,'result.csv'),'a')

if len(img_list)==0:
    print("No file exist at %s" % img_root)
    sys.exit(0)
print("### %d files are found at %s." % (len(img_list),img_root))


for img_no,img_path in enumerate(img_list):
    print("Processing (%d/%d) : %s" % (img_no+1,len(img_list),img_path))

    ###
    ### RUN ONLINE MODEL ###
    ###    

    error_flag=""
    while error_flag!='success':
        result_raw=modelderm(server_url,unique_id,img_path).decode('unicode_escape')
        result_raw_split_=result_raw.split(',')
        error_flag=result_raw_split_[0]
        if error_flag[0:4].lower()=='wait':
            print("Failed : %s" % (result_raw))
            currentusers_,message_=get_server_status(server_url,unique_id)
            currentusers_=int(currentusers_)
            if currentusers_>0:print("Wait for %d users." % (currentusers_))
            while currentusers_>0:
                time.sleep(2)
                currentusers_,message_=get_server_status(server_url,unique_id)
                currentusers_=int(currentusers_)
                if currentusers_>0:print("Wait for %d users." % (currentusers_))
            print("RESUME")
        elif error_flag!='success':
            print("Failed : %s" % (result_raw))
            sys.exit(1)

    ###
    ### RECEIVE PREDEFINED THRESHOLDS
    ###
    engine_version=result_raw_split_[1]
    threshold_high_se=float(result_raw_split_[2]) # high sensitivity threshold
    threshold_high_sp=float(result_raw_split_[3]) # high specificity threshold
    print(engine_version,threshold_high_se,threshold_high_sp)
    ### FOR DISPLAY
    stream=open(img_path,'rb')
    img_display = cv2.imdecode(np.asarray(bytearray(stream.read()), dtype=np.uint8), cv2.IMREAD_UNCHANGED)

    ###
    ### BOXES, MALIGNANCY OUTPUT, PREDICTION ('-' = nonspecific)
    ###
    rcnn_infos=result_raw[result_raw.find('['):]
    for no_,rcnn_info in enumerate(rcnn_infos[:-1].split(']')):
        x0,y0,x1,y1,malignancy_output,prediction=rcnn_info[1:].split(',')
        x0=int(x0)
        x1=int(x1)
        y0=int(y0)
        y1=int(y1)
        malignancy_output=float(malignancy_output)

        print(no_,x0,y0,x1,y1,malignancy_output,prediction)
        f_result.write('%s,%d' % (img_path.replace(img_root,""),no_))
        f_result.write(',%d,%d,%d,%d' % (x0,y0,x1,y1))
        f_result.write(',%f,%s\n' % (malignancy_output,prediction))


        ###
        ### DRAW RECT
        ###

        #thin gray
        color_=(50,50,50)
        bold_=1
        if malignancy_output>threshold_high_se: 
            #bold orange
            color_=(30,144,255)
            bold_=3
        if malignancy_output>threshold_high_sp: 
            #bold red
            color_=(0,0,255)
            bold_=3
        cv2.rectangle(img_display,(x0,y0),(x1,y1),color_,bold_)

        font = cv2.FONT_HERSHEY_TRIPLEX
        fontScale = 2
        color_=(0,0,0)
        bold_=2
        cv2.putText(img_display,'%d %s'% (int(malignancy_output*100),prediction),(x0,y0),font,fontScale,color_,bold_)

    dest_path=img_path.replace(img_root,dest_root)
    try:os.makedirs(os.path.dirname(dest_path))
    except:pass
    print("Image saved at ",dest_path)
    cv2.imwrite(os.path.join(dest_path),img_display)

f_result.close()
print("Images and csv result files are saved at ",dest_root)    
print("FINISHED")    
