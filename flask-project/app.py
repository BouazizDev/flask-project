from flask import Flask,render_template,request,redirect,url_for,flash

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np
import shutil,os
import random, string
app = Flask(__name__)
app.secret_key = 'lalalal'
def randName(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
    

@app.route('/', methods=['GET'])
def display():
    return render_template('index.html')


@app.route('/', methods=['POST'])

def predict():
    if(os.path.isfile("./images/img.jpg")):
        os.remove("./images/img.jpg")
    imagefile= request.files['imagefile']
    originalImgPath = "./images/" + imagefile.filename
    imagefile.save(originalImgPath)
    os.rename(originalImgPath,r"./images/img.jpg")
    imgPath = "./images/img.jpg"
    
    # loading the model 
    model = tensorflow.keras.models.load_model('keras_model.h5')
    #image preprocessing 
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    image = Image.open(imgPath)
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.ANTIALIAS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.0) - 1
    data[0] = normalized_image_array
    prediction = model.predict(data)
    classification  = 'carie : (%.2f%%) bout de racine : (%.2f%%) radiculaire : (%.2f%%) ' %(prediction[0][0]*100,prediction[0][1]*100, prediction[0][2]*100 ) 

    return redirect(url_for('confirm', prediction = classification ))
@app.route('/confirm',methods=["GET","POST"])
def confirm():
    if request.method == "GET":
        return render_template("confirmation.html" , prediction = request.args.get("prediction"))  
    src1 = r"./images/img.jpg"
    src = "./images/{}.jpg".format(randName())
    os.rename(src1,src)
    dest1 = r'./train/carie'  
    dest2 = r'./train/bout de racine'  
    dest3 = r'./train/radiculaire'  
    if request.method == "POST":
        req = request.form.getlist("mycheckbox")
        for x in req:
            if x == '1':
                shutil.copy(str(src),dest1)
            if x == '2':
                shutil.copy(str(src),dest2)
            if x == '3':
                shutil.copy(str(src),dest3)
        os.remove(src)
        flash('l''étiquette est changée avec succès')
        return render_template("confirmation.html")




   




if __name__ == '__main__' :
    app.run(port=3003,debug=True)