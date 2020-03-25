
import PIL
from PIL import Image
load = Image.open
import os
import pandas as pd
from os.path import join
import numpy as np
import sys

from matplotlib import pyplot as plt

folder = sys.argv[1]

# In[ ]:


datadict = {'s'+str(i):os.listdir(os.path.join(folder,'s'+str(i))) for i in range(1,41)}
gen = ((int(name[1:]),name,img,int(img.split('.')[0])) for name in datadict for img in datadict[name])
df = pd.DataFrame(gen,columns=['id','person','image_name','im_num'])
df['image_paths'] = df.apply(lambda x: join(folder, x['person'], x['image_name']), axis=1)
df['image'] = df['image_paths'].apply(lambda x: load(x))
original_shape = np.array(df.image[0]).shape


# In[ ]:


df['array'] = df.image.apply(lambda x: np.array(x).reshape((-1,1)))


# In[ ]:


avg_face = np.mean((df.loc[df['im_num']<=5])['array'],axis=0) #only take first halves for training


# In[ ]:


df['diff'] = df['array'].apply(lambda x: x-avg_face)


# In[ ]:


df_train = df.loc[df['im_num']<=5].copy()
df_test = df.loc[df['im_num']>5].copy()
df_train.reset_index(drop=True, inplace=True)
df_test.reset_index(drop=True, inplace=True)
df_train.shape, df_test.shape


# In[ ]:


A = np.concatenate(df_train['diff'],axis=1)
A.shape


# In[ ]:


L = np.matmul(A.T,A)
L.shape


# In[ ]:


eigen_vals, v = np.linalg.eig(L)
eigen_vals.shape, v.shape


# In[ ]:


idx = eigen_vals.argsort()[::-1]   
eigen_vals = eigen_vals[idx]
v = v[:,idx]


# In[ ]:


u = np.matmul(A,v)
u.shape


# In[ ]:


U = u/np.linalg.norm(u, ord=2, axis=0, keepdims=True)
U.shape


# In[ ]:


def plottable_eigen_face(face_column):
    arr = face_column.reshape(original_shape)
    arr -= arr.min()
    arr *= 255/arr.max()
    img = Image.fromarray(arr)
    return img


# In[ ]:

# plot first 20 eigenfaces

rows = 4
columns = 5
fig, axes = plt.subplots(nrows=rows, ncols=columns,figsize=(15,10))
for i in range(rows):
    for j in range(columns):
        axes[i,j].imshow(plottable_eigen_face(u[:,(i*columns)+j]),cmap='gray', vmin=0, vmax=255)
        axes[i,j].title.set_text('E.' + str((i*columns)+j+1))
        axes[i,j].axis('off')
fig.suptitle('First 20 eigen faces')

# In[ ]:


one_image = df_test.loc[(df_test['id']==8) & (df_test['im_num']==8)]
oi_et = np.matmul(U.T, one_image['diff'].iloc[0])




# In[ ]:


def plot_eigen_face(face_column):
    arr = face_column.reshape(original_shape)
    arr -= arr.min()
    arr *= 255/arr.max()
    img = Image.fromarray(arr)
    plt.imshow(img)

def reconstruct_image(transformed_image, eigen_face_vectors, size):
    recim = np.zeros_like(eigen_face_vectors[:,0])
    for i in range(size):
        recim += transformed_image[i,0] * eigen_face_vectors[:,i]
    return recim


# In[ ]:

# reconstruct a face

faces = []
sizes = [2, 5, 10, 20, 40, 60, 100, 150, 200]
for size in sizes:
    recim = reconstruct_image(oi_et, U[:,0:size], size)
    faces.append(recim)

rows = 2
columns = 5
fig, axes = plt.subplots(nrows=rows, ncols=columns,figsize=(15,10))
for i in range(rows):
    for j in range(columns):
        try:
            axes[i,j].imshow( plottable_eigen_face(faces[(i*columns)+j]), cmap='gray', vmin=0, vmax=255 )
            axes[i,j].title.set_text(str(sizes[i*columns+j]))
            axes[i,j].axis('off')
        except IndexError:
            axes[i,j].imshow( one_image['image'].iloc[0], cmap='gray', vmin=0, vmax=255 )
            axes[i,j].title.set_text('original')
            axes[i,j].axis('off')
fig.suptitle('Reconstruction of s8 8.pgm')
    


# In[ ]:


df_train['projection'] = df_train['diff'].apply(lambda diff : np.matmul(U.T, diff))
df_test['projection'] = df_test['diff'].apply(lambda diff : np.matmul(U.T, diff))


# In[ ]:


def NN(person_vector,size):
    distances = []
    for index, (vector, person) in df_train[['projection','person']].iterrows():        
        dist = np.linalg.norm(vector[:size,:] - person_vector[:size,:])
        distances.append((dist,person))
    return min(distances,key=lambda x : x[0])


# In[ ]:


def evaluate(size):
    variance_explnd = sum(eigen_vals[:size])/sum(eigen_vals)
    win=0
    loss=0
    for _, (test_vector, test_person) in df_test[['projection','person']].iterrows():
        _, closest = NN(test_vector, size)
        if closest == test_person:
            win+=1
        else:
            loss+=1
    return win, loss


# In[ ]:

# size = 100
size = int(sys.argv[2])
w, l = evaluate(size)
print('For', size, 'eigen faces identification rate is', w/(w+l))


plt.show()
    

