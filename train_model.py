
import os, pickle
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.layers import GlobalAveragePooling2D, Dense, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau

IMG_SIZE=(224,224)
BATCH_SIZE=32
EPOCHS=20

train_dir="dataset/train"
val_dir="dataset/validation"
test_dir="dataset/test"

train_gen=ImageDataGenerator(preprocessing_function=preprocess_input,
                             rotation_range=20,zoom_range=0.2,
                             horizontal_flip=True)
test_gen=ImageDataGenerator(preprocessing_function=preprocess_input)

train=train_gen.flow_from_directory(train_dir,target_size=IMG_SIZE,batch_size=BATCH_SIZE,class_mode="categorical")
val=test_gen.flow_from_directory(val_dir,target_size=IMG_SIZE,batch_size=BATCH_SIZE,class_mode="categorical",shuffle=False)
test=test_gen.flow_from_directory(test_dir,target_size=IMG_SIZE,batch_size=BATCH_SIZE,class_mode="categorical",shuffle=False)

base=MobileNetV2(weights="imagenet",include_top=False,input_shape=(224,224,3))
base.trainable=False

x=GlobalAveragePooling2D()(base.output)
x=Dropout(0.3)(x)
out=Dense(train.num_classes,activation="softmax")(x)
model=Model(base.input,out)

model.compile(optimizer="adam",loss="categorical_crossentropy",metrics=["accuracy"])

os.makedirs("model",exist_ok=True)
os.makedirs("static/images",exist_ok=True)

cb=[
EarlyStopping(patience=5,restore_best_weights=True),
ReduceLROnPlateau(patience=2,factor=0.2),
ModelCheckpoint("model/mobilenetv2_model.keras",save_best_only=True)
]

history=model.fit(train,validation_data=val,epochs=EPOCHS,callbacks=cb)

with open("model/class_names.pkl","wb") as f:
    pickle.dump(list(train.class_indices.keys()),f)

acc=history.history["accuracy"]; vacc=history.history["val_accuracy"]
loss=history.history["loss"]; vloss=history.history["val_loss"]

plt.figure()
plt.plot(acc); plt.plot(vacc)
plt.legend(["Train","Validation"]); plt.title("Accuracy")
plt.savefig("static/images/accuracy.png"); plt.close()

plt.figure()
plt.plot(loss); plt.plot(vloss)
plt.legend(["Train","Validation"]); plt.title("Loss")
plt.savefig("static/images/loss.png"); plt.close()

print(model.evaluate(test))
print("Training selesai.")
