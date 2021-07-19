from flask import Flask,render_template,request

import tensorflow.keras
from PIL import Image, ImageOps
import numpy as np

app = Flask(__name__)

@app.route('/', methods=['GET'])
def display():
    return render_template('index.html')

@app.route('/', methods=['POST'])

def predict():
    imagefile= request.files['imagefile']
    imgPath = "./images/" + imagefile.filename
    imagefile.save(imgPath)
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

    return render_template('index.html' , prediction = classification )


if __name__ == '__main__' :
    app.run(port=3003,debug=True)