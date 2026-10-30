from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
from django.http import HttpResponse
import datetime
import ipfsApi
import os
import json
from web3 import Web3, HTTPProvider
from django.core.files.storage import FileSystemStorage
import pickle
import random
import pyaes, pbkdf2, binascii, os, secrets
import base64
import sqlite3
import time
import matplotlib.pyplot as plt
import mimetypes
import numpy as np
import smtplib
from email.message import EmailMessage
from datetime import datetime, timedelta
import shutil
import csv
import cv2
import face_recognition
import numpy as np
import pandas as pd
import sqlite3
import PrivacyChainApp.train_faces as trainface
import cv2
import pickle
import face_recognition
from datetime import datetime
import sqlite3 
import time

api = ipfsApi.Client(host='http://127.0.0.1', port=5001)
global details, username, access_user

runtime_data = []
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages(id,name):
    estest=0
    #print estest
    if (estest==0):
        if(is_number(id) and name.isalpha()):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector=cv2.CascadeClassifier(harcascadePath)
            sampleNum=0
            img_counter = 0
            DIR=f"./Dataset/{name}_{id}"
            try:
                os.mkdir(DIR)
                print("Directory " , name ,  " Created ") 
            except FileExistsError:
                print("Directory " , name ,  " already exists")
                img_counter = len(os.listdir(DIR))
            while(True):
                ret, frame = cam.read()
                cv2.imshow("Video", frame)
                if not ret:
                    break
                k = cv2.waitKey(1)
                if k%256 == 27:
                    # ESC pressed
                    print("Escape hit, closing...")
                    break
                elif k%256 == 32:
                    # SPACE pressed
                    img_name = f"./Dataset/{name}_{id}/opencv_frame_{img_counter}.png"
                    cv2.imwrite(img_name, frame)
                    print("{} written!".format(img_name))
                    img_counter += 1
            cam.release()
            cv2.destroyAllWindows()
            res = "Captured Image" 
            
            
        else:
            if(is_number(id)):
                res = "Enter Alphabetical Name"
                
            if(name.isalpha()):
                res = "Enter Numeric Id"
               
        
    else:
        res = "Already Id Exist"
    return res

def getKey(): #generating key with PBKDF2 for AES
    password = "s3cr3t*c0d3"
    passwordSalt = '76895'
    key = pbkdf2.PBKDF2(password, passwordSalt).read(32)
    return key
def to_datetime(datestring):
    return datetime.strptime(datestring, '%d-%b-%Y %H:%M:%S')
def encrypt(plaintext): #AES data encryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    ciphertext = aes.encrypt(plaintext)
    return ciphertext

def decrypt(enc): #AES data decryption
    aes = pyaes.AESModeOfOperationCTR(getKey(), pyaes.Counter(31129547035000047302952433967654195398124239844566322884172163637846056248223))
    decrypted = aes.decrypt(enc)
    return decrypted

def readDetails(contract_type):
    global details
    details = ""
    print(contract_type+"======================")
    blockchain_address = 'http://127.0.0.1:9545' #Blokchain connection IP
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'AuthPrivacyChain.json' #Blockchain AuthPrivacyChain contract code
    deployed_contract_address = '0x063C4901100ebFb592EAb6c745D31F263D39281c' #hash address to access AuthPrivacyChain contract
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi) #now calling contract to access data
    if contract_type == 'signup':
        details = contract.functions.getDataUser().call()
    if contract_type == 'direct':
        details = contract.functions.getDirectSharing().call()
    if contract_type == 'indirect':
        details = contract.functions.getInDirectSharing().call()
    if contract_type == 'timedata':
        details = contract.functions.gettime().call()     
    print(details)    

def saveDataBlockChain(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'AuthPrivacyChain.json' #Blockchain contract file
    deployed_contract_address =  '0x063C4901100ebFb592EAb6c745D31F263D39281c' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.createDataUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'direct':
        details+=currentData
        msg = contract.functions.setDirectSharing(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'indirect':
        details+=currentData
        msg = contract.functions.setInDirectSharing(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'timedata':
        details+=currentData
        msg = contract.functions.settime(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)

def saveDataBlockChain1(currentData, contract_type):
    global details
    global contract
    details = ""
    blockchain_address = 'http://127.0.0.1:9545'
    web3 = Web3(HTTPProvider(blockchain_address))
    web3.eth.defaultAccount = web3.eth.accounts[0]
    compiled_contract_path = 'AuthPrivacyChain.json' #Blockchain contract file
    deployed_contract_address = '0x063C4901100ebFb592EAb6c745D31F263D39281c' #contract address
    with open(compiled_contract_path) as file:
        contract_json = json.load(file)  # load contract info as JSON
        contract_abi = contract_json['abi']  # fetch contract's abi - necessary to call its functions
    file.close()
    contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)
    #readDetails(contract_type)
    if contract_type == 'signup':
        details+=currentData
        msg = contract.functions.createDataUser(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'direct':
        details+=currentData
        msg = contract.functions.setDirectSharing(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)
    if contract_type == 'indirect':
        details+=currentData
        msg = contract.functions.setInDirectSharing(details).transact()
        tx_receipt = web3.eth.waitForTransactionReceipt(msg)        

def RevokeUser(request):
    if request.method == 'GET':
        readDetails('direct')
        arr = details.split("\n")
        output = '<tr><td><font size="" color=white>Choose&nbsp;File&nbsp;To&nbsp;Revoke&nbsp;User</b></td>'
        output +='<td><select name="t1">'
        files = []
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[0] == username and array[2] not in files:
                files.append(array[2])
                output += '<option value="'+array[2]+'">'+array[2]+'</option>'
        output += "</select></td></tr>"
        context= {'data':output}
        return render(request, 'RevokeUser.html', context)

def RevokeUserAction(request):
    if request.method == 'POST':
        global username
        filename = request.POST.get('t1', False)
        readDetails('direct')
        arr = details.split("\n")
        data = ""
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[2] != filename:
                data += arr[i]+"\n"
        saveDataBlockChain1(data,"direct")
        output = 'Users revoke from selected file : '+filename
        context= {'data':output}
        return render(request, 'DataOwnerScreen.html', context) 

def Download(request):
    global username, access_user,details
    cam=cv2.VideoCapture(0)
    fname=identify_faces(cam)
    if request.method == 'GET':
        if fname==username:
            filename = request.GET['t1']
            print("Filename==",filename)
            hashcode = request.GET['t2']
            useres=request.GET['t3']
            if access_user in useres:
                readDetails('timedata')
                arr = details.split("\n")
                status = "none"
                sdate=""
                cdate=""
                for i in range(len(arr)-1):
                    array = arr[i].split("#")
                    print("Array of timedata==",array)
                    if array[1] == username and array[5]==filename:
                        sdate=array[2]
                        cdate=array[3]
                        break
                print("sdate==",sdate)
                print("cdate=",cdate)
                now = datetime.now()
                yesterday = to_datetime(str(sdate))
                tomorrow = to_datetime(str(cdate))
                print("yesterday==",yesterday)
                print("today=",now)
                print("tomorrow==",tomorrow)
                if yesterday < now < tomorrow:
                    content = api.get_pyobj(hashcode)
                    content = pickle.loads(content)
                    content = decrypt(content)
                    mime_type, _ = mimetypes.guess_type(filename)
                    response = HttpResponse(content, content_type=mime_type)
                    response['Content-Disposition'] = "attachment; filename=%s" % filename
                    return response
                else:
                    output="Time expired for this file"
                    context= {'data':output}
                    return render(request, 'AccessShareData.html', context)

            else:
                output="Your are not having access control for this file"
                context= {'data':output}
                return render(request, 'AccessShareData.html', context)
        else:
            output="Your face is not matched"
            context= {'data':output}
            return render(request, 'AccessShareData.html', context)

def settime(request):
    if request.method=='GET':
        global username
        readDetails('direct')
        arr = details.split("\n")
        print("Arr[0]==",arr[0])
        
        output = '<table border=1 align=center width=100%><tr><th><font size="" color="black">Data Owner Name</th><th><font size="" color="black">Filename</th>'
        output+='<th><font size="" color="black">Set Time</th>'
        files = []
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            print("Array==",array)
            if str(array[0])==str(username):
                if array[2] not in files:
                    files.append(array[2])
                    output+='<tr><td><font size="" color="black">'+str(array[0])+'</td><td><font size="" color="black">'+array[2]+'</td>'
                    output+='<td><a href="settimeuser?t1='+array[0]+'&t2='+array[2]+'"><font size="" color="black">Click Here</a></td>'
                    context= {'data':output}
                    #return render(request, 'settimepage.html', context)
                else:
                    output="No Files Shared"
                    context= {'data':output}

        return render(request, 'DataOwnerScreen.html', context)
def settimeuser(request):
    if request.method=='GET':
        global username,access_user,filename
        filename = request.GET['t2']
        ownername=request.GET['t1']
        readDetails('signup')
        userslist=[]
        arr = details.split("\n")
        status = "none"
        output = []
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] != ownername and array[3] != access_user:
                
                 output.append( array[1])
                 
                 #return render(request, 'settimeactionpage.html', context)
            else:
                continue
        
        context= {'data':output}
        return render(request, 'settimeactionpage.html',context)
def settimetouseraction(request):
    if request.method=='POST':
        global username,filename,details
        user_nam=request.POST.getlist('t1', False)
        sdate=request.POST.get('sdate', False)
        cdate=request.POST.get('cdate', False)
        for user in user_nam:
            print("uname==",user)
            print("sdate==",sdate)
            print("cdate==",cdate)
            print("ownername==",username)
            print("Filename==",filename)
            status = "none"
            readDetails('timedata')
            arr = details.split("\n")
            status = "none"
            for i in range(len(arr)-1):
                array = arr[i].split("#")
                if array[1] == user and array[5]==filename:
                    output = user_nam+" Time Already set for this user"
                    break
                if status == "none":
                    data = "settime#"+user+"#"+sdate+"#"+cdate+"#"+username+"#"+filename+"\n"
                    saveDataBlockChain(data,"timedata")
                    output = "Set Time task completed User Details saved in Blockchain"
                    
            context= {'data':output}
            return render(request,'settimepage.html', context)
        else:
            context= {'data':output}
            return render(request,'settimepage.html',context)
        


            





def AccessShareData(request):
    if request.method == 'GET':
        #global username, access_user
        readDetails('direct')
        arr = details.split("\n")
        print("Arr[0]==",arr[0])
        if arr[0]!='':
            output = '<table border=1 align=center width=100%><tr><th><font size="" color="black">Data Owner Name</th><th><font size="" color="black">Filename</th>'
            output+='<th><font size="" color="black">Blockchain Hash Value</th><th><font size="" color="black">Access Permission Users</th>'
            output+='<th><font size="" color="black">Upload Date Time</th>'
            output+='<th><font size="" color="black">Download & View Data</th></tr>'
            files = []
        
            for i in range(len(arr)-1):
                array = arr[i].split("#")
                print("Array==",array)
                if array[2] not in files:
                    files.append(array[2])
                    output+='<tr><td><font size="" color="black">'+str(array[0])+'</td><td><font size="" color="black">'+array[2]+'</td><td><font size="" color="black">'+str(array[4])+'</td>'
                    output+='<td><font size="" color="black">'+str(array[1])+'</td>'
                    output+='<td><font size="" color="black">'+str(array[3])+'</td>'
                    output+='<td><a href="Download?t1='+array[2]+'&t2='+array[4]+'&t3='+array[1]+'"><font size="" color="black">Click Here</a></td>'
                    context= {'data':output}
            return render(request, 'AccessShareData.html', context)
        else:
            output="No Files Shared"
            context= {'data':output}
            return render(request, 'AccessShareData.html', context)

        
def viewnotification(request):
    if request.method == 'GET':
        global username, access_user
        
        output = '<table border=1 align=center width=100%><tr><th><font size="" color="black">Data Owner Name</th><th><font size="" color="black">Filename</th>'
        output+='<th><font size="" color="black">User Name</th>'
        files = []
        conn= sqlite3.connect("db.sqlite3")
        cmd="SELECT * FROM indirectaccess WHERE ownername='"+username+"'"
        cursor=conn.execute(cmd)
        for row in cursor:
            print("row=",row)
            output+='<tr><td><font size="" color="black">'+str(row[1])+'</td><td><font size="" color="black">'+row[0]+'</td>'
            output+='<td><font size="" color="black">'+str(row[2])+'</td>'
        context= {'data':output}
        return render(request, 'DataOwnerScreen.html', context)

def Graph(request):
    global runtime_data
    if request.method == 'GET':
        height = []
        bars = []
        for i in range(len(runtime_data)):
            arr = runtime_data[i].split(",")
            bars.append(arr[0])
            height.append(float(arr[1]))
        y_pos = np.arange(len(bars))
        plt.bar(y_pos, height)
        plt.xticks(y_pos, bars)
        plt.title("Blockchain Total Computation Time for Storage & Access Permission")
        plt.show()
        context= {'data':"Computation Graph"}
        return render(request, 'DataUserScreen.html', context)
    
    

def IndirectAccessAction(request):
    if request.method == 'POST':
        global username,details
        filename = request.POST.get('t1', False)
        print("Filename==",filename)
        readDetails('direct')
        arr = details.split("\n")
        conn= sqlite3.connect("db.sqlite3")
        data = ""
        ownername=""
        email=""
        found = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[2] != filename:
                data += arr[i]+"\n"
                ownername=array[0]
            else:
                data += array[0]+"#Doctor Researcher#"+array[2]+"#"+array[3]+"#"+array[4]+"\n"
                ownername=array[0]
        print("owner name=",ownername)
        readDetails('signup')
        arr1 = details.split("\n")
        for j in range(len(arr1)-1):
            array1 = arr1[j].split("#")
            if array1[1]==ownername:
                email=array1[4]
                break
        print("Owner email==",email)
        saveDataBlockChain1(data,"direct")
        output = 'indirect access given to other user for file : '+filename
        cmd="INSERT INTO indirectaccess Values('"+str(filename)+"','"+str(array[0])+"','"+str(username)+"')"
        print(cmd)
        msg=EmailMessage()
        msg.set_content("Indirect Access Given for your File "+str(filename)+" By "+str(username))
        msg['Subject']='Notification'
        msg['From']="mindsparkblore@gmail.com"
        msg['to']=email
        s=smtplib.SMTP('smtp.gmail.com',587)
        s.starttls()
        s.login("mindsparkblore@gmail.com","djscowxdrtnlmock")
        s.send_message(msg)
        s.quit()
        print("Inserted Successfully")
        conn.execute(cmd)
        conn.commit()
        conn.close()
        context= {'data':output}
        return render(request, 'DataUserScreen.html', context)  


def IndirectAccess(request):
    if request.method == 'GET':
        global username, access_user
        readDetails('direct')
        arr = details.split("\n")
        output = '<tr><td><font size="" color=black>Choose&nbsp;File&nbsp;For&nbsp;Indirect&nbsp;Access</b></td>'
        output +='<td><select name="t1">'
        files = []
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            print(access_user+" "+array[1]+" "+str(access_user in array[1]))
            if access_user in array[1] and array[2] not in files:
                files.append(array[2])
                output += '<option value="'+array[2]+'">'+array[2]+'</option>'
        output += "</select></td></tr>"
        context= {'data':output}
        return render(request, 'IndirectAccess.html', context)


def UploadImageAction(request):
    if request.method == 'POST':
        global username,runtime_data
        start = time.time()
        access = request.POST.getlist('t2')
        access = ' '.join(access)
        access = access.strip()
        filename = request.FILES['t1'].name
        myfile = request.FILES['t1'].read()
        myfile = encrypt(myfile)
        myfile = pickle.dumps(myfile)
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        hashcode = api.add_pyobj(myfile)
        data = username+"#"+access+"#"+str(filename)+"#"+str(current_time)+"#"+str(hashcode)+"\n"
        saveDataBlockChain(data,"direct")
        end = time.time()
        runtime_data.append(filename+","+str(end-start))
        output = 'Given medical file saved in cloud with hash code.<br/>'+str(hashcode)
        context= {'data':output}
        return render(request, 'UploadImage.html', context)        
    
def UploadImage(request):
    if request.method == 'GET':
       return render(request, 'UploadImage.html', {})
    
def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Login(request):
    if request.method == 'GET':
       return render(request, 'Login.html', {})

def Signup(request):
    if request.method == 'GET':
       return render(request, 'Signup.html', {})
def predict(rgb_frame, knn_clf=None, model_path=None, distance_threshold=0.5):

    if knn_clf is None and model_path is None:
        raise Exception("Must supply knn classifier either thourgh knn_clf or model_path")

    # Load a trained KNN model (if one was passed in)
    if knn_clf is None:
        with open(model_path, 'rb') as f:
            knn_clf = pickle.load(f)

    # Load image file and find face locations
    # X_img = face_recognition.load_image_file(X_img_path)
    X_face_locations = face_recognition.face_locations(rgb_frame, number_of_times_to_upsample=2)

    # If no faces are found in the image, return an empty result.
    if len(X_face_locations) == 0:
        return []

    # Find encodings for faces in the test iamge
    faces_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations=X_face_locations)

    # Use the KNN model to find the best matches for the test face
    closest_distances = knn_clf.kneighbors(faces_encodings, n_neighbors=1)
    are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(X_face_locations))]
    # print(closest_distances)
    # Predict classes and remove classifications that aren't within the threshold
    return [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(knn_clf.predict(faces_encodings), X_face_locations, are_matches)]



def identify_faces(video_capture):

    buf_length = 10
    known_conf = 5
    buf = [[]] * buf_length
    i = 0

    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_frame = np.ascontiguousarray(small_frame[:, :, ::-1])

        if process_this_frame:
            predictions = predict(rgb_frame, model_path="./models/trained_model.clf")
            # print(predictions)

        process_this_frame = not process_this_frame

        face_names = []
        current_date=datetime.today().strftime('%Y-%m-%d')

        for name, (top, right, bottom, left) in predictions:

            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
            print("Recognized name==",name)
            if name!="UNKNOWN" or name!="unknown" or name!="UnKnown":
               return name
               break



            #identify1(frame, name, buf, buf_length, known_conf)

            face_names.append(name)

        buf[i] = face_names
        i = (i + 1) % buf_length


        # print(buf)


        # Display the resulting image
        cv2.imshow('In Camera', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
def LoginAction(request):
    if request.method == 'POST':
        global username, access_user
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        usertype = request.POST.get('t3', False)
        cam=cv2.VideoCapture(0)
        fname=identify_faces(cam)
        if fname==username:
            readDetails('signup')
            arr = details.split("\n")
            status = "none"
            for i in range(len(arr)-1):
                array = arr[i].split("#")
                if array[1] == username and password == array[2] and array[3] == usertype:
                    status = "Welcome "+username
                    access_user = usertype
                    break
            if status != 'none' and usertype == 'Data Owner':
                context= {'data':status}
                return render(request, 'DataOwnerScreen.html', context)
            elif status != 'none' and usertype == 'Doctor':
                context= {'data':status}
                return render(request, 'DataUserScreen.html', context)
            elif status != 'none' and usertype == 'Researcher':
                context= {'data':status}
                return render(request, 'DataUserScreen.html', context)
            else:
                context= {'data':'login failed'}
                return render(request, 'Login.html', context)
        else:
            context= {'data':'Face Not Matched'}
            return render(request, 'Login.html', context)


        
def SignupAction(request):
    if request.method == 'POST':
        global details
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        uid=0
        
        usertype = request.POST.get('t3', False)
        email=request.POST.get('t4',False)
        output = "Username already exists"
        readDetails('signup')
        arr = details.split("\n")
        status = "none"
        for i in range(len(arr)-1):
            array = arr[i].split("#")
            if array[1] == username:
                status = username+" already exists"
                break
        if status == "none":
            details = ""
            data = "signup#"+username+"#"+password+"#"+usertype+"#"+email+"\n"
            saveDataBlockChain(data,"signup")
            output=TakeImages(int(uid),username)
            context = {"data":"Signup process completed and record saved in Blockchain and Face Image Taken"}
            trainface.trainer()
            return render(request, 'Signup.html', context)
        else:
            context = {"data":status}
            return render(request, 'Signup.html', context)
