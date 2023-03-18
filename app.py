from flask import Flask, redirect,render_template,request, session
import os
from hashlib import sha512
import uuid
import cv2
import pandas as pd
import numpy as np
import tensorflow_hub as hub
from tensorflow.keras.models import load_model
import pickle
import json
f = open('data.json')
data_vendors = json.load(f)
# print(list(filter(lambda x: x['original'] == 'potato',data_vendors)))
app = Flask(__name__)
image_model_path = './Soil_Analysis/my_model.h5'
image_model = load_model(image_model_path,custom_objects={'KerasLayer':hub.KerasLayer})
AVG_SOIL_VALUES = pd.read_csv("to_save_ang.csv")
df=pd.read_csv('./to_save_ang_li.csv')

def load_model(model_name):
    with open(model_name, "rb") as file:
        model = pickle.load(file)
    return model
CROPS_MODEL = load_model("crop_rec.pkl")
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
            val = "BLACK"
            if input_label == 0:
                val = "BLACK"
            elif input_label == 1:
                val = "CINDER"
            elif input_label == 2:
                val = "LATERITE"
            elif input_label == 3:
                val = "PEAT"
            elif input_label == 4:
                val = "YELLOW"
            nx = np.array([AVG_SOIL_VALUES[val]])
            t = nx.reshape(1, -1)
            distances, indices = CROPS_MODEL.kneighbors(t, n_neighbors=5)
            rec = set()
            for i in indices[0]:
                rec.add(df.iloc[i]['label'])
            # return rec.__str__()
            to_re = []
            for i in rec:
                to_re.append(list(filter(lambda x: x['original'] == i,data_vendors)))
            return to_re.__str__()
        except Exception as e:
            print(e)
            return "error"
    else:
        return "error"

if __name__ == '__main__':
    app.run(debug=True)