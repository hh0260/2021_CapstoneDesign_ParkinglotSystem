# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 18:21:02 2021

@author: hh026
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential

#print(tf.version.VERSION)

import pathlib

cwd = os.getcwd() #작업 중인 디렉토리

data_dir = pathlib.Path(cwd+"/train_data")  

image_count = len(list(data_dir.glob('*/*.jpg')))  #총 이미지 개수
print("total img: " + str(image_count))
 
#몇가지 매개변수 정의
batch_size = 32
img_height = 100
img_width = 200

#8:2로 검증 분할
train_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="training",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

val_ds = tf.keras.preprocessing.image_dataset_from_directory(
  data_dir,
  validation_split=0.2,
  subset="validation",
  seed=123,
  image_size=(img_height, img_width),
  batch_size=batch_size)

#각 속성별 이름
class_names = train_ds.class_names
print(class_names)

#훈련 데이터셋 이미지 시각화하기


plt.figure(figsize=(10, 10))
for images, labels in train_ds.take(1):
  for i in range(9):
    ax = plt.subplot(3, 3, i + 1)
    plt.imshow(images[i].numpy().astype("uint8"))
    plt.title(class_names[labels[i]])
    plt.axis("off")

#이미지, 라벨 확인    
for image_batch, labels_batch in train_ds:
  print(image_batch.shape)
  print(labels_batch.shape)
  break

#셔플
AUTOTUNE = tf.data.experimental.AUTOTUNE
train_ds = train_ds.cache().shuffle(1000).prefetch(buffer_size=AUTOTUNE)
val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)

#0~255를 0~1로 정규화
normalization_layer = layers.experimental.preprocessing.Rescaling(1./255)

normalized_ds = train_ds.map(lambda x, y: (normalization_layer(x), y))
image_batch, labels_batch = next(iter(normalized_ds))
first_image = image_batch[0]
# Notice the pixels values are now in `[0,1]`.
print(np.min(first_image), np.max(first_image))

###모델 만들기 시작###

num_classes = 2 #속성 개수

model = Sequential([
  layers.experimental.preprocessing.Rescaling(1./255, input_shape=(img_height, img_width, 3)),
  layers.Conv2D(16, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(32, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Conv2D(64, 3, padding='same', activation='relu'),
  layers.MaxPooling2D(),
  layers.Flatten(),
  layers.Dense(128, activation='relu'),
  layers.Dense(num_classes)
])

model.compile(optimizer='adam',
              loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
              metrics=['accuracy'])

model.summary()   #모델 요약

epochs=13    #모델 훈련하기
history = model.fit(
  train_ds,
  validation_data=val_ds,
  epochs=epochs
)

model.save('parking_model.h5')  #모델 저장하기

# 훈련결과 시각화
acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss=history.history['loss']
val_loss=history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()


#실제 데이터로 테스트

sunflower_path = cwd+"/test_images/car/007.jpg"

img = keras.preprocessing.image.load_img(
    sunflower_path, target_size=(img_height, img_width)
)
print(img)
print(type(img))

img_array = keras.preprocessing.image.img_to_array(img)
print(img_array)
print(type(img_array))

img_array = tf.expand_dims(img_array, 0) # Create a batch
print(img_array)
print(type(img_array))
predictions = model.predict(img_array)
score = tf.nn.softmax(predictions[0])

print(class_names[np.argmax(score)])
print(np.argmax(score))
print(100 * np.max(score))


'''
# 모델 구조를 출력합니다
new_model.summary()

img_array2 = keras.preprocessing.image.img_to_array(img)
img_array2 = tf.expand_dims(img_array2, 0) # Create a batch

predictions = model.predict(img_array2)
score = tf.nn.softmax(predictions[0])

print(class_names[np.argmax(score)])
print(100 * np.max(score))

'''

#개선사항1. 학습데이터 밤이든 저녁이든 낮이든 추가 학습필요

