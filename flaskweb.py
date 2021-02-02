import cv2
from flask import Flask, render_template, Response, request,jsonify,redirect
import numpy as np


app = Flask(__name__)

@app.route('/')
def upload_image():
    return render_template('upload_image.html')

@app.route('/index.html')
def index():
    return render_template('index.html')



@app.route('/video')
def video():
    return Response(gen_magicam(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/show_pic.html')
def show_pic():
    return render_template('show_pic.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/save_frame',methods=['GET','POST'])
def save_frames():
    while camera.isOpened():
        ret, frame = camera.read() #reading from cam  ### read mobile cam using flutter
        if request.method=='POST':
            if ret:
                   ###we will add flutter click button to capture image 
                    # save the image
                cv2.imwrite('image.jpg', frame)#### return clicked img to flutter project
                break
    return redirect('/')


camera = cv2.VideoCapture(0)
def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result




def magicam():
    frame = cv2.imread('./image.jpg')
    while camera.isOpened():
        #take each frame
        ret, pic = camera.read()
       
        if ret:
                #how to convt rgb to hsv
            hsv = cv2.cvtColor(pic, cv2.COLOR_BGR2HSV)
                #cv2.imshow("hsv",hsv)
                #how to get the hsv value?
                #lower: hue -10,100,100, heigher: h+10, 255, 255
            red = np.uint8([[[0,0,0]]])#bgr value of red
            hsv_red = cv2.cvtColor(red, cv2.COLOR_BGR2HSV)
                #print hsv value of red from bgr 
                #print(hsv_red)
                

                #threshold the hsv value to get only red colors
            l_red = np.array([0,0,0])
            u_red = np.array([180,255, 30])
                
            mask = cv2.inRange(hsv, l_red,u_red)
                #cv2.imshow("mask",mask)

                #all things red
            part1 = cv2.bitwise_and(frame, frame, mask=mask)
                #cv2.imshow("part1",part1)

            mask = cv2.bitwise_not(mask)
                
                #part2 all thing not red 
            part2 = cv2.bitwise_and(pic, pic, mask=mask)
                #cv2.imshow("mask",part2)
                
            part3 = part1 + part2

            ret, jpeg = cv2.imencode('.jpg', part3)
            return jpeg.tobytes()           
            # yield (b'--frame\r\n'
            #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            
def gen_magicam():
    while True:
        #get camera frame
        frame = magicam()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')




if __name__ == "__main__":
    app.run(debug=False)