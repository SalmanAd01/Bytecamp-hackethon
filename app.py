from flask import Flask, redirect,render_template,request, session
import os
from hashlib import sha512
import uuid
import cv2
import numpy as np
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
app = Flask(__name__)
image_model_path = './Soil_Analysis/my_model.h5'
image_model = load_model(image_model_path,custom_objects={'KerasLayer':hub.KerasLayer})
@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/image/upload',methods=['GET','POST'])
def image_upload():
    if request.method == 'POST':
        try:
            file = request.files['file']
            file_extension = os.path.splitext(file.filename)[1]
            file_name = str(file.filename)+uuid.uuid4().hex
            file_name = file_name.encode('utf-8')
            hash_filename = sha512(file_name).hexdigest()+str(file_extension)
            file.save(os.path.join('images', hash_filename))
            img_test = cv2.imread(os.path.join('images', hash_filename))
            img_resize = cv2.resize(img_test,(224,224))
            img_scaled = img_resize/255
            img_reshaped = np.reshape(img_scaled,[1,224,224,3])
            input_pred = image_model.predict(img_reshaped)
            input_label = np.argmax(input_pred)
            if input_label == 0:
                return "Black Soil"
            elif input_label == 1:
                return "Cinder Soil"
            elif input_label == 2:
                return "Laterite Soil"
            elif input_label == 3:
                return "Peat Soil"
            elif input_label == 4:
                return "Yellow Soil"
            return "success"
        except Exception as e:
            print(e)
            return "error"
    else:
        return "error"

if __name__ == '__main__':
    app.run(debug=True)