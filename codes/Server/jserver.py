import pymysql, os, time, json
from datetime import datetime
from flask import Flask, request, session, render_template, jsonify, redirect

app = Flask(__name__)
# app.secret_key = b'switch.wizice!'
#app.secret_key = b'switch.chan!'
file_path = 'C:\project files\Capstone_Design\data.json'
setting_path='C:\project files\Capstone_Design\setting.json'



#db select함수
#--------------------------------auto--------------------------------------------------------------

#--------------------------------main--------------------------------------------------------------
@app.route('/main', methods=['GET', 'POST'])
def mn():
    now=datetime.now()
    data={}
    settingData={}
#      while True:
    try:
        a_json = open(file_path, encoding='utf8')
        data=json.load(a_json)
        a_json2 = open(setting_path, encoding='utf8')
        settingData=json.load(a_json2)
        
    except:
        print("mn!!!!!!!!!!!!!!!!!")
        time.sleep(0.5)
        mn()

    settingName=["foodS1","foodS2","foodS3","lampOffS","lampOnS"]
    dataName=["food","food","food","lamp","lamp"]
    dataVal=["1","1","1","0","1"]

    for i in range(5):
        if settingData[settingName[i]] != "0" and data["mode"] == "1":
            s=settingData[settingName[i]].split("h")
            if now.hour==int(s[0]) and now.minute==int(s[1]) and now.second==0:
                data[dataName[i]]=dataVal[i]
                with open(file_path, 'w', encoding='utf-8') as file:
                    json.dump(data, file)
                    file.close()  
    if settingData["tempS"] != "0" and data["mode"] == "1":
        if (int(settingData["tempS"]))+1<=int(float(data["temp"])):
            data["heater"]="0"
            data["fan1"]="1"
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file)
                file.close()
        if (int(settingData["tempS"]))-1>=int(float(data["temp"])):
            data["heater"]="1"
            data["fan1"]="0"
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file)
                file.close()
        if (int(settingData["tempS"]))==int(float(data["temp"])):
            data["heater"]="0"
            data["fan1"]="0"
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file)
                file.close()

    return data
#--------------------------------input--------------------------------------------------------------
@app.route('/input', methods=['GET', 'POST'])
def sen_inp():#수정해야함
    param = request.args.to_dict()
    a_json = open(file_path, encoding='utf8')
    jsda=json.load(a_json)
    print(jsda)
    param = request.args.to_dict()
    print(param)
    for jval in jsda:
        for val in param:
            if jval == val:
                jsda[jval] =param[val]
    print(jsda)
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(jsda, file)
        file.close()
    return jsda

#--------------------------------getSetting--------------------------------------------------------------
@app.route('/getSetting', methods=['GET', 'POST'])
def getSetting():
    data={}
#      while True:
    try:
        a_json = open(setting_path, encoding='utf8')
        data=json.load(a_json)
    except:
        print("getSetting!!!!!!!!!!!!!!!!!")
        time.sleep(0.5)
        getSetting()
    return data 

#--------------------------------input--------------------------------------------------------------
@app.route('/inputSetting', methods=['GET', 'POST'])
def inputSetting():#수정해야함
    param = request.args.to_dict()
    a_json = open(setting_path, encoding='utf8')
    jsda=json.load(a_json)
    print(jsda)
    param = request.args.to_dict()
    print(param)
    for jval in jsda:
        for val in param:
            if jval == val:
                jsda[jval] =param[val]
    print(jsda)
    with open(setting_path, 'w', encoding='utf-8') as file:
        json.dump(jsda, file)
        file.close()
    return jsda
#--------------------------------appCam--------------------------------------------------------------
@app.route('/appCam', methods=['GET', 'POST'])
def appcam():
     return render_template("appCam.html")
# 파이썬 명령어로 실행할 수 있음
if __name__ == '__main__':
    
    app.run(host='0.0.0.0',port=5000, debug=True,threaded=True)#port 개방
#     app.run(port=5000, debug=True)