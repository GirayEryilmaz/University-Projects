#!/usr/bin/env python3
# coding: utf-8

# In[2]:


import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    def __init__(self, input_texts, target_texts, input_token_index, target_token_index, max_encoder_seq_length, max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens, batch_size, shuffle=True):
        'Initialization'
        self.input_texts = input_texts
        self.target_texts = target_texts
        self.batch_size = batch_size
        self.shuffle = shuffle
        self.input_token_index = input_token_index
        self.target_token_index = target_token_index
        self.max_encoder_seq_length = max_encoder_seq_length
        self.max_decoder_seq_length = max_decoder_seq_length
        self.num_encoder_tokens = num_encoder_tokens
        self.num_decoder_tokens = num_decoder_tokens
        self.on_epoch_end()


    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.input_texts) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        input_text_sample = [self.input_texts[x] for x in indexes]
        target_text_sample = [self.target_texts[x] for x in indexes]

        # Generate data
        X, y = self.__data_generation(input_text_sample, target_text_sample)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        self.indexes = np.arange(len(self.input_texts))
        if self.shuffle == True:
            np.random.shuffle(self.indexes)

    def __data_generation(self, input_text_sample, target_text_sample):
        'Generates data containing batch_size samples' # X : (n_samples, *dim, n_channels)
        # Initialization
        encoder_input_data = np.zeros(
            (len(input_text_sample), self.max_encoder_seq_length, self.num_encoder_tokens),
            dtype='float32')
        decoder_input_data = np.zeros(
            (len(input_text_sample), self.max_decoder_seq_length, self.num_decoder_tokens),
            dtype='float32')
        decoder_target_data = np.zeros(
            (len(input_text_sample), self.max_decoder_seq_length, self.num_decoder_tokens),
            dtype='float32')

        for i, (input_text, target_text) in enumerate(zip(input_text_sample, target_text_sample)):
            for t, char in enumerate(input_text):
                encoder_input_data[i, t, self.input_token_index[char]] = 1.
            for t, char in enumerate(target_text):
                # decoder_target_data is ahead of decoder_input_data by one timestep
                decoder_input_data[i, t, self.target_token_index[char]] = 1.
                if t > 0:
                    # decoder_target_data will be ahead by one timestep
                    # and will not include the start character.
                    decoder_target_data[i, t - 1, target_token_index[char]] = 1.
        
        
        return [encoder_input_data, decoder_input_data], decoder_target_data


# In[3]:


# from __future__ import print_function
import keras
from keras.models import Model
from keras.layers import Input, Dense, CuDNNLSTM
from keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
import pickle
import matplotlib.pyplot as plt 

from keras.models import load_model


# In[4]:


batch_size = 512  # Batch size for training.
epochs = 50 #100  # Number of epochs to train for.
latent_dim = 256  # Latent dimensionality of the encoding space.
# Path to the data txt file on disk.


# In[5]:


data_path = 'sarcastics_only.csv'
df = pd.read_csv(data_path, usecols=['parent_comment','comment'])
# df['comment'] = df['comment'].apply(lambda x: x.replace("\n", " ").join(['\t','\n']))
#punctuation spacele split


# In[6]:


input_texts = []
target_texts = []

input_characters = set()
target_characters = set()
for idx in range(len(df)):
    target_text = df["comment"][idx]
    input_text = df["parent_comment"][idx]
    
    target_text = ' '.join(df["comment"][idx].split())[:200]
    input_text = ' '.join(df["parent_comment"][idx].split())[:200]
    target_text = target_text.join(['\t','\n'])
    
    target_texts.append(target_text)
    input_texts.append(input_text)
    for char in input_text:
        if char not in input_characters:
            input_characters.add(char)
    for char in target_text:
        if char not in target_characters:
            target_characters.add(char)


# In[7]:


input_token_index = dict(
    [(char, i) for i, char in enumerate(input_characters)])
target_token_index = dict(
    [(char, i) for i, char in enumerate(target_characters)])


# In[8]:

#input_texts = input_texts[:1000]
#target_texts = target_texts[:1000]


train_input_texts, valid_input_texts, train_target_texts, valid_target_texts = train_test_split(input_texts, target_texts, test_size=0.1, random_state=42)
del input_texts, target_texts, df


# In[9]:


input_characters = sorted(list(input_characters))
target_characters = sorted(list(target_characters))
num_encoder_tokens = len(input_characters)
num_decoder_tokens = len(target_characters)
max_encoder_seq_length = max(max([len(txt) for txt in train_input_texts]), max([len(txt) for txt in valid_input_texts]))
max_decoder_seq_length = max(max([len(txt) for txt in train_target_texts]), max([len(txt) for txt in valid_target_texts]))
print('Number of samples:', len(train_input_texts))
print('Number of unique input tokens:', num_encoder_tokens)
print('Number of unique output tokens:', num_decoder_tokens)
print('Max sequence length for inputs:', max_encoder_seq_length)
print('Max sequence length for outputs:', max_decoder_seq_length)


# In[10]:


training_generator = DataGenerator(train_input_texts, train_target_texts, input_token_index, target_token_index, max_encoder_seq_length, max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens, batch_size)
validation_generator = DataGenerator(valid_input_texts, valid_target_texts, input_token_index, target_token_index, max_encoder_seq_length, max_decoder_seq_length, num_encoder_tokens, num_decoder_tokens, batch_size)


# In[11]:


encoder_inputs = Input(shape=(None, num_encoder_tokens))
encoder = CuDNNLSTM(latent_dim, return_state=True)
encoder_outputs, state_h, state_c = encoder(encoder_inputs)
# We discard `encoder_outputs` and only keep the states.
encoder_states = [state_h, state_c]

# Set up the decoder, using `encoder_states` as initial state.
decoder_inputs = Input(shape=(None, num_decoder_tokens))
# We set up our decoder to return full output sequences,
# and to return internal states as well. We don't use the
# return states in the training model, but we will use them in inference.
decoder_lstm = CuDNNLSTM(latent_dim, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_inputs,
                                     initial_state=encoder_states)
decoder_dense = Dense(num_decoder_tokens, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

model = Model([encoder_inputs, decoder_inputs], decoder_outputs)


# In[12]:


model.compile(optimizer='rmsprop', loss='categorical_crossentropy', metrics=['accuracy'])


# In[13]:


earlyStopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1, mode='min')
mcp_save = ModelCheckpoint('.mdl_wts.hdf5', save_best_only=True, monitor='val_loss', mode='min')
reduce_lr_loss = ReduceLROnPlateau(monitor='val_loss', factor=0.1, patience=7, verbose=1, mode='min')


history = model.fit_generator(generator=training_generator,
                    validation_data=validation_generator,
                    epochs=epochs,
                    callbacks=[earlyStopping, mcp_save, reduce_lr_loss],
                    verbose=1)



# In[16]:



# Plot training & validation accuracy values
# try:
#     plt.plot(history.history['acc'])
#     plt.plot(history.history['val_acc'])
#     plt.title('Model accuracy')
#     plt.ylabel('Accuracy')
#     plt.xlabel('Epoch')
#     plt.legend(['Train', 'Test'], loc='upper left')
#     plt.show()
#     plt.savefig('acc.png')
#     plt.savefig('acc.pdf')
# except:
#     print('failed on acc plot')

# Plot training & validation loss values
try:
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig('loss.png')
    plt.savefig('loss.pdf')
except:
    print('failed on loss plot')   


# In[17]:


#save etcd
model.save('s2s.h5')


# In[18]:



# Define sampling models
sampler_encoder_model = Model(encoder_inputs, encoder_states)

sampler_decoder_state_input_h = Input(shape=(latent_dim,))
sampler_decoder_state_input_c = Input(shape=(latent_dim,))
sampler_decoder_states_inputs = [sampler_decoder_state_input_h, sampler_decoder_state_input_c]
sampler_decoder_outputs, sampler_state_h, sampler_state_c = decoder_lstm(
    decoder_inputs, initial_state=sampler_decoder_states_inputs)
sampler_decoder_states = [sampler_state_h, sampler_state_c]
sampler_decoder_outputs = decoder_dense(sampler_decoder_outputs)

sampler_decoder_model = Model(
    [decoder_inputs] + sampler_decoder_states_inputs,
    [sampler_decoder_outputs] + sampler_decoder_states)


# In[19]:


sampler_encoder_model.save('sampler_encoder_model.h5')
sampler_decoder_model.save('sampler_decoder_model.h5')


# In[20]:


with open('target_token_index.pickle', 'wb') as pf:
    pickle.dump(target_token_index, pf, protocol=pickle.HIGHEST_PROTOCOL)

with open('input_token_index.pickle', 'wb') as pf:
    pickle.dump(input_token_index, pf, protocol=pickle.HIGHEST_PROTOCOL)

# num_decoder_tokens, 


# In[21]:


variables = {'num_encoder_tokens':num_encoder_tokens,
             'num_decoder_tokens':num_decoder_tokens,
             'max_encoder_seq_length':max_encoder_seq_length,
             'max_decoder_seq_length':max_decoder_seq_length
            }

with open('variables.pickle', 'wb') as pf:
    pickle.dump(variables, pf, protocol=pickle.HIGHEST_PROTOCOL)


# In[ ]:


print('Done')
