# -*- coding: utf-8 -*-
"""Model1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16pVIEmsr9-eO4pHidjjuBhIDpphphctR
"""

import numpy as np
import pandas as pd
from keras.layers import Input, Dense, Embedding, Conv2D, MaxPool2D
from keras.layers import Reshape, Flatten, Dropout, Concatenate
from keras.callbacks import ModelCheckpoint
from keras.optimizers import Adam
from keras.models import Model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, Conv1D, MaxPooling1D, Dropout, Activation
from sklearn.model_selection import train_test_split
import time
from keras import optimizers

!apt-get install -y -qq software-properties-common python-software-properties module-init-tools
!add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
!apt-get update -qq 2>&1 > /dev/null
!apt-get -y install -qq google-drive-ocamlfuse fuse
from google.colab import auth
auth.authenticate_user()
from oauth2client.client import GoogleCredentials
creds = GoogleCredentials.get_application_default()
import getpass
!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
vcode = getpass.getpass()
!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

!mkdir -p drive
!google-drive-ocamlfuse drive -o nonempty

import os
os.chdir('drive')

#data_train = pd.read_csv('v1/Preprocessed_using_translator_train.csv')
data_train = pd.read_csv('Preprocessed_using_translator_train.csv')
data_train.shape

#data_test= pd.read_csv("v1/Preprocessed_using_translator_test.csv")
data_test= pd.read_csv("Preprocessed_using_translator_test.csv")
data_test.shape

tokenize = Tokenizer(num_words= 10)
tokenize.fit_on_texts(['Hello, today is a good day hello Hello hi!'])
sequencd = tokenize.texts_to_sequences(['Hello, is today a good!'])
print(sequencd)
data = pad_sequences(sequencd)
print(data)

print(tokenize)

data_train["text"] = data_train["text"].apply(str)
data_test["text"] = data_test["text"].apply(str)
ylabels = pd.get_dummies(data_train.iloc[:,2].values)
vocabulary_size = 10000 
tokenizer = Tokenizer(num_words= vocabulary_size)
tokenizer.fit_on_texts(data_train["text"].values)
sequences = tokenizer.texts_to_sequences(data_train["text"].values)
data = pad_sequences(sequences)

xtrain, xval, ytrain, yval = train_test_split(data, ylabels, test_size=0.10, random_state=960)
print(xtrain.shape, xval.shape, ytrain.shape, yval.shape)

sequence_length = data.shape[1]
embedding_dim = 76
num_filters = 32
filter_sizes = [33, 33, 33]
drop = 0.2

inputs = Input(shape=(sequence_length,), dtype='int32')
embedding = Embedding(input_dim=vocabulary_size, output_dim=embedding_dim, input_length=sequence_length)(inputs)
reshape = Reshape((sequence_length,embedding_dim,1))(embedding)

c0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
c1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
c2 = Conv2D(num_filters, kernel_size=(filter_sizes[2], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)

DP0 = MaxPool2D(pool_size=(sequence_length - filter_sizes[0] + 1, 1), strides=(1,1), padding='valid')(c0)
DP1 = MaxPool2D(pool_size=(sequence_length - filter_sizes[1] + 1, 1), strides=(1,1), padding='valid')(c1)
DP2 = MaxPool2D(pool_size=(sequence_length - filter_sizes[2] + 1, 1), strides=(1,1), padding='valid')(c2)

CT = Concatenate(axis=1)([DP0, DP1, DP2])

flatten = Flatten()(CT)
dropout = Dropout(drop)(flatten)
output = Dense(units=3, activation='softmax')(dropout)

batch_size=32
epochs = 10

model = Model(inputs=inputs, outputs=output)

checkpoint = ModelCheckpoint('weights.{epoch:03d}-{val_acc:.4f}.hdf5', monitor='val_acc', verbose=1, save_best_only=True, mode='auto')
adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)

model.compile(optimizer=adam, loss='categorical_crossentropy', metrics=['accuracy'])

st = time.time()
model.fit(xtrain, ytrain, batch_size=batch_size, epochs=epochs, verbose=1, callbacks=[checkpoint], validation_data=(xval, yval))  # starts training
en = time.time()

sequencesTest = tokenizer.texts_to_sequences(data_test["text"].values)
dataTest = pad_sequences(sequencesTest, maxlen=988)
print(data.shape)
print(dataTest.shape)

print(dataTest.shape)

sequence_length = data.shape[1]
embedding_dim = 76
num_filters = 32
filter_sizes = [33, 33, 33]
drop = 0.2

inputs = Input(shape=(sequence_length,), dtype='int32')
embedding = Embedding(input_dim=vocabulary_size, output_dim=embedding_dim, input_length=sequence_length)(inputs)
reshape = Reshape((sequence_length,embedding_dim,1))(embedding)

c0 = Conv2D(num_filters, kernel_size=(filter_sizes[0], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
c1 = Conv2D(num_filters, kernel_size=(filter_sizes[1], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)
c2 = Conv2D(num_filters, kernel_size=(filter_sizes[2], embedding_dim), padding='valid', kernel_initializer='normal', activation='relu')(reshape)

DP0 = MaxPool2D(pool_size=(sequence_length - filter_sizes[0] + 1, 1), strides=(1,1), padding='valid')(c0)
DP1 = MaxPool2D(pool_size=(sequence_length - filter_sizes[1] + 1, 1), strides=(1,1), padding='valid')(c1)
DP2 = MaxPool2D(pool_size=(sequence_length - filter_sizes[2] + 1, 1), strides=(1,1), padding='valid')(c2)

CT = Concatenate(axis=1)([DP0, DP1, DP2])

flatten = Flatten()(CT)
dropout = Dropout(drop)(flatten)
output = Dense(units=3, activation='softmax')(dropout)

batch_size=32
epochs = 10

model = Model(inputs=inputs, outputs=output)

model.load_weights("hello.hdf5")

yPred = model.predict(dataTest, verbose = 1)
answer = np.argmax(yPred,axis=1)

newdataTest = pd.DataFrame({ 'label':answer})
newdataTest.index += 1
newdataTest.to_csv("Submission.csv")

newdataTest["label"].value_counts()

