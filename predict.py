import os
import pickle
import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input

# ==========================
# Konfigurasi
# ==========================
MODEL_PATH = "model/mobilenetv2_model.keras"
CLASS_PATH = "model/class_names.pkl"

IMG_SIZE = (224, 224)

# ==========================
# Load Model
# ==========================
model = load_model(MODEL_PATH)

with open(CLASS_PATH, "rb") as f:
    class_names = pickle.load(f)


# ==========================
# Deskripsi Setiap Kelas
# ==========================
class_description = {

    "Dress":
        "Dress merupakan pakaian wanita yang menutupi tubuh bagian atas hingga bawah.",

    "Hat":
        "Hat adalah penutup kepala yang digunakan sebagai pelindung maupun aksesoris.",

    "Longsleeve":
        "Longsleeve merupakan pakaian berlengan panjang.",

    "Outwear":
        "Outwear adalah pakaian luar seperti jaket atau hoodie.",

    "Pants":
        "Pants merupakan celana panjang.",

    "Shirt":
        "Shirt adalah kemeja dengan kerah dan kancing.",

    "Shoes":
        "Shoes merupakan alas kaki.",

    "Shorts":
        "Shorts adalah celana pendek.",

    "Skirt":
        "Skirt merupakan rok.",

    "T-Shirt":
        "T-Shirt adalah kaos berlengan pendek."
}


# ==========================
# Preprocessing
# ==========================
def preprocess_image(image_path):

    image = Image.open(image_path)

    image = image.convert("RGB")

    image = image.resize(IMG_SIZE)

    image = np.array(image)

    image = preprocess_input(image)

    image = np.expand_dims(image, axis=0)

    return image


# ==========================
# Prediksi
# ==========================
def predict(image_path):

    image = preprocess_image(image_path)

    prediction = model.predict(image, verbose=0)

    probabilities = prediction[0]

    predicted_index = np.argmax(probabilities)

    predicted_class = class_names[predicted_index]

    confidence = float(probabilities[predicted_index] * 100)

    description = class_description.get(
        predicted_class,
        "Tidak ada deskripsi."
    )

    probability_list = []

    for i, class_name in enumerate(class_names):

        probability_list.append({

            "class": class_name,

            "probability": round(float(probabilities[i] * 100), 2)

        })

    probability_list = sorted(

        probability_list,

        key=lambda x: x["probability"],

        reverse=True

    )

    result = {

        "prediction": predicted_class,

        "confidence": round(confidence, 2),

        "description": description,

        "probabilities": probability_list

    }

    return result


# ==========================
# Testing
# ==========================
if __name__ == "__main__":

    image_path = "sample.jpg"

    if os.path.exists(image_path):

        result = predict(image_path)

        print("=" * 40)

        print("Prediction :", result["prediction"])

        print("Confidence :", result["confidence"], "%")

        print(result["description"])

        print("=" * 40)

        print("\nSemua Probabilitas:\n")

        for item in result["probabilities"]:

            print(

                f"{item['class']:15}"

                f"{item['probability']:.2f}%"

            )

    else:

        print("sample.jpg tidak ditemukan.")