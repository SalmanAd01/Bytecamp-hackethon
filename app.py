from flask import Flask, redirect, render_template, request, session
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

f = open("data.json")
data_vendors = json.load(f)
# print(list(filter(lambda x: x['original'] == 'potato',data_vendors)))
app = Flask(__name__)
image_model_path = "./Soil_Analysis/my_model.h5"
image_model = load_model(
    image_model_path, custom_objects={"KerasLayer": hub.KerasLayer}
)
AVG_SOIL_VALUES = pd.read_csv("to_save_ang.csv")
df = pd.read_csv("./to_save_ang_li.csv")
import pickle

filename = "model.pkl"
with open(filename, "rb") as f:
    yield_model = pickle.load(f)


def load_model(model_name):
    with open(model_name, "rb") as file:
        model = pickle.load(file)
    return model


CROPS_MODEL = load_model("crop_rec.pkl")


def mah(Area, dist_name, season, crop):
    mah_dict = {
        "Area": 0,
        "District_Name_AHMEDNAGAR": 0,
        "District_Name_AKOLA": 0,
        "District_Name_AMRAVATI": 0,
        "District_Name_AURANGABAD": 0,
        "District_Name_BEED": 0,
        "District_Name_BHANDARA": 0,
        "District_Name_BULDHANA": 0,
        "District_Name_CHANDRAPUR": 0,
        "District_Name_DHULE": 0,
        "District_Name_GADCHIROLI": 0,
        "District_Name_GONDIA": 0,
        "District_Name_HINGOLI": 0,
        "District_Name_JALGAON": 0,
        "District_Name_JALNA": 0,
        "District_Name_KOLHAPUR": 0,
        "District_Name_LATUR": 0,
        "District_Name_MUMBAI": 0,
        "District_Name_NAGPUR": 0,
        "District_Name_NANDED": 0,
        "District_Name_NANDURBAR": 0,
        "District_Name_NASHIK": 0,
        "District_Name_OSMANABAD": 0,
        "District_Name_PALGHAR": 0,
        "District_Name_PARBHANI": 0,
        "District_Name_PUNE": 0,
        "District_Name_RAIGAD": 0,
        "District_Name_RATNAGIRI": 0,
        "District_Name_SANGLI": 0,
        "District_Name_SATARA": 0,
        "District_Name_SINDHUDURG": 0,
        "District_Name_SOLAPUR": 0,
        "District_Name_THANE": 0,
        "District_Name_WARDHA": 0,
        "District_Name_WASHIM": 0,
        "District_Name_YAVATMAL": 0,
        "Season_Autumn     ": 0,
        "Season_Kharif     ": 0,
        "Season_Rabi       ": 0,
        "Season_Summer     ": 0,
        "Season_Whole Year ": 0,
        "Crop_Arhar/Tur": 0,
        "Crop_Bajra": 0,
        "Crop_Banana": 0,
        "Crop_Castor seed": 0,
        "Crop_Cotton(lint)": 0,
        "Crop_Gram": 0,
        "Crop_Grapes": 0,
        "Crop_Groundnut": 0,
        "Crop_Jowar": 0,
        "Crop_Linseed": 0,
        "Crop_Maize": 0,
        "Crop_Mango": 0,
        "Crop_Moong(Green Gram)": 0,
        "Crop_Niger seed": 0,
        "Crop_Onion": 0,
        "Crop_Other  Rabi pulses": 0,
        "Crop_Other Cereals & Millets": 0,
        "Crop_Other Kharif pulses": 0,
        "Crop_Pulses total": 0,
        "Crop_Ragi": 0,
        "Crop_Rapeseed &Mustard": 0,
        "Crop_Rice": 0,
        "Crop_Safflower": 0,
        "Crop_Sesamum": 0,
        "Crop_Small millets": 0,
        "Crop_Soyabean": 0,
        "Crop_Sugarcane": 0,
        "Crop_Sunflower": 0,
        "Crop_Tobacco": 0,
        "Crop_Tomato": 0,
        "Crop_Total foodgrain": 0,
        "Crop_Urad": 0,
        "Crop_Wheat": 0,
        "Crop_other oilseeds": 0,
    }
    mah_dict["Area"] = Area
    mah_dict[dist_name] = 1
    mah_dict[season] = 1
    mah_dict[crop] = 1
    data = list(mah_dict.values())
    print(mah_dict)
    input_arr = np.array(data)
    return input_arr


@app.route("/")
def hello_world():
    return render_template("index.html")


@app.route("/image/upload", methods=["GET", "POST"])
def image_upload():
    if request.method == "POST":
        try:
            file = request.files["file"]
            file_extension = os.path.splitext(file.filename)[1]
            file_name = str(file.filename) + uuid.uuid4().hex
            file_name = file_name.encode("utf-8")
            hash_filename = sha512(file_name).hexdigest() + str(file_extension)
            file.save(os.path.join("images", hash_filename))
            img_test = cv2.imread(os.path.join("images", hash_filename))
            img_resize = cv2.resize(img_test, (224, 224))
            img_scaled = img_resize / 255
            img_reshaped = np.reshape(img_scaled, [1, 224, 224, 3])
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
                rec.add(df.iloc[i]["label"])
            # return rec.__str__()
            to_re = []
            for i in rec:
                to_re.append(list(filter(lambda x: x["original"] == i, data_vendors)))
            return render_template("crop.html", soil_type=val, crops=rec)
        except Exception as e:
            print(e)
            return "error"
    else:
        return "error"


@app.route("/vendor/<name>")
def vendor(name):
    to_re = []
    to_re.append(list(filter(lambda x: x["original"] == name, data_vendors)))
    # to_re.sort(key=lambda x: x["standardPrice"].split("/")[0], reverse=True)
    print(to_re)

    return render_template("vendors.html", vendors=to_re[0])


@app.route("/yeild")
def yeild_recommend():
    data = request.get_json()
    distname = data["distname"]
    season = data["season"]
    crop = data["crop"]
    print(distname, season, crop)
    arr=mah(31500,'District_Name_'+distname,season,crop)
    pre = yield_model.predict([arr])
    print(pre)
    return pre.__str__()


if __name__ == "__main__":
    app.run(debug=True)
