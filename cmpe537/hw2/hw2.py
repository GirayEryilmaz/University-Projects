#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np


import matplotlib; matplotlib.use('TkAgg') #this has to be before importing plt

from matplotlib import pyplot as plt

from PIL import Image

import os


# In[ ]:


north_campus_image_paths = {
    "l2":"north_campus/left-2.jpg",
    "l1":"north_campus/left-1.jpg",
    "m":"north_campus/middle.jpg",
    "r1":"north_campus/right-1.jpg",
    "r2":"north_campus/right-2.jpg",
}

building_paths = {
    "l2":"cmpe-building/left-2.jpg",
    "l1":"cmpe-building/left-1.jpg",
    "m":"cmpe-building/middle.jpg",
    "r1":"cmpe-building/right-1.jpg",
    "r2":"cmpe-building/right-2.jpg",
}


# In[ ]:


def click_select(img, n=-1, timeout=0,title="Choose points"):
    # negative n means no limits
    fig = plt.figure()
    if isinstance(img, str):
        img = plt.imread(img)
    plt.imshow(img)
    plt.title(title)
    points = plt.ginput(n, show_clicks=True, timeout=timeout)
    plt.close()
    return np.array(points).T

def to_homogenous_coords(points):
    return np.vstack((points, np.ones(points.shape[1])))

def get_normalization_matrix(points):
    m1 = points[0, :].mean() # mean of x's
    m2 = points[1, :].mean() # mean of y's
    p = np.linalg.norm(points, axis=1).mean() / np.sqrt(2)
    
    translation_matrix = np.array(((1, 0, -m1),
                                   (0, 1, -m2),
                                   (0, 0,  1 )), dtype=np.float)

    scale = np.reciprocal(p, dtype=np.float)
    scale_matrix = np.array(((scale, 0,   0),
                             (0,   scale, 0),
                             (0,     0,   1)), dtype=np.float)
    
    return np.matmul(scale_matrix, translation_matrix)


# In[ ]:


def homography_estimation(points1, points2):

    n = points1.shape[1]
    d = points1.shape[0]
    A = np.zeros([2 * n, 3 * d]) # start empty this is faster that stacking up normal lists

    odd_idx = [i % 2 == 1 for i in range(2 * n)]
    even_idx = [i % 2 == 0 for i in range(2 * n)]

    A[even_idx, :d] = points1.T
    A[odd_idx, d: 2 * d] = points1.T

    temp = np.zeros([2 * n, d])
    temp[even_idx] = points1.T
    temp[odd_idx] = points1.T


    A[:, -d:] = -1 * (points2[:-1, :].T.flatten()[:, np.newaxis] * temp)

    _, _, Vt = np.linalg.svd(A, full_matrices=True)

    H = Vt[-1, :].reshape(d, d)

    return H


# In[ ]:


def warp(orig_image, H):
    """
    orig_im = to morph
    """
    H_inv = np.linalg.inv(H)
    extrm_points = find_morphed_corner_values(orig_image, H)
    width = (extrm_points['maxx'] - extrm_points['minx'])
    height = (extrm_points['maxy'] - extrm_points['miny'])


    im_arr = np.zeros((width, height,3)) #note that h and w are reversed in Image objects I guess

    # must form a matrix and multiply it with h_inv with numpy. for loop takes forever
    y_range = np.arange(extrm_points['miny'], extrm_points['maxy'])
    x_range = np.arange(extrm_points['minx'], extrm_points['maxx'])

    xv, yv = np.meshgrid(x_range, y_range, indexing="ij") # fancy mesh generating function
    x_coords = xv.flatten()
    y_coords = yv.flatten()
    ones = np.ones(height*width) # z=1 for making into hom coords

    all_points = np.stack((x_coords,
                          y_coords,
                          ones))

    morphed_p = np.matmul(H_inv, all_points)

    morphed_p = morphed_p/(morphed_p[2,:])

    morphed_p = morphed_p.astype(np.int)

    def interpolate(back_x, back_y, orig_image):
        back_x = int(np.rint(back_x))
        back_y = int(np.rint(back_y))
        return  orig_image.getpixel((int(back_x),int(back_y)))

    for i, x in enumerate(x_range):
        for j, y in enumerate(y_range):
            back_x, back_y , _ = tuple(morphed_p[:,i*height+j])
            if back_x >= 0 and back_y>=0 and back_x<orig_image.width and back_y< orig_image.height:
                im_arr[x-extrm_points['minx'], y-extrm_points['miny'],:] = interpolate(back_x, back_y, orig_image)


    return Image.fromarray(np.swapaxes(im_arr,0,1).astype('uint8')), extrm_points, im_arr
    


# In[ ]:


def computeH(im1Points, im2Points, normalize=True):
    
    homogenous_points1 = to_homogenous_coords(im1Points)
    homogenous_points2 = to_homogenous_coords(im2Points)

    if not normalize:
        return homography_estimation(homogenous_points1, homogenous_points2)
    
    norm_mat_im1 = get_normalization_matrix(homogenous_points1)
    norm_mat_im2 = get_normalization_matrix(homogenous_points2)

    normalized_points1 = np.matmul(norm_mat_im1, homogenous_points1)
    normalized_points2 = np.matmul(norm_mat_im2, homogenous_points2)
    
    if normalize:
        return np.matmul(np.linalg.pinv(norm_mat_im2), np.matmul(homography_estimation(normalized_points1, normalized_points2), norm_mat_im1))
    # else:
    #     return homography_estimation(homogenous_points1, homogenous_points2)
    
def find_morphed_corner_values(image, H):
    corner = np.array([[image.width-1],[image.height-1],[1]])
    new_corner = np.matmul(H, corner)
    new_corner = new_corner/new_corner[2,0]
    max_x = max(np.zeros(1)[0], new_corner[0, 0])
    max_y = max(np.zeros(1)[0], new_corner[1, 0])
    minx = min(np.zeros(1)[0], new_corner[0, 0])
    miny = min(np.zeros(1)[0], new_corner[1, 0])

    unscaled = np.matmul(H, np.array([[0],[image.height-1],[1]]))
    scaled = unscaled/unscaled[2,0]
    max_x = max(max_x, scaled[0, 0])
    max_y = max(max_y, scaled[1, 0])
    minx = min(minx, scaled[0, 0])
    miny = min(miny, scaled[1, 0])

    unscaled = np.matmul(H, np.array([[image.width-1],[0],[1]]))
    scaled = unscaled/unscaled[2,0]
    max_x = max(max_x, scaled[0, 0])
    max_y = max(max_y, scaled[1, 0])
    minx = min(minx, scaled[0, 0])
    miny = min(miny, scaled[1, 0])

    unscaled = np.matmul(H, np.array([[0],[0],[1]]))
    scaled = unscaled/unscaled[2,0]
    max_x = max(max_x, scaled[0, 0]).astype(np.int)
    max_y = max(max_y, scaled[1, 0]).astype(np.int)
    minx = min(minx, scaled[0, 0]).astype(np.int)
    miny = min(miny, scaled[1, 0]).astype(np.int)
    return {'maxx': max_x, 'minx':minx, 'maxy':max_y, 'miny':miny}


# In[ ]:


def merge_3_ims(path_l, path_m, path_r, n, load_points=False, save_points=False, noise_scale=0, normalize=True, title=''):
    
    if not load_points:
        p_l = click_select(path_l, n, title=title)
        p_m_for_l = click_select(path_m, n, title=title)

        p_r = click_select(path_r, n, title=title)
        p_m_for_r = click_select(path_m, n, title=title)

    if load_points:
        p_l = np.load('p_l.npy')
        p_m_for_l = np.load('p_m_for_l.npy')
        p_r = np.load('p_r.npy')
        p_m_for_r = np.load('p_m_for_r.npy')

    
    if noise_scale:
        p_l += np.random.rand(*p_l.shape)*noise_scale
        p_m_for_l += np.random.rand(*p_m_for_l.shape)*noise_scale
        p_r += np.random.rand(*p_r.shape)*noise_scale
        p_m_for_r += np.random.rand(*p_m_for_r.shape)*noise_scale
            
        
    if save_points:
        np.save('p_l.npy', p_l)
        np.save('p_m_for_l.npy', p_m_for_l)
        np.save('p_r.npy', p_r)
        np.save('p_m_for_r.npy', p_m_for_r)
        
    
    H_l_to_m = computeH(p_l, p_m_for_l, normalize=normalize)
    H_r_to_m = computeH(p_r, p_m_for_r, normalize=normalize)

    l = Image.open(path_l)
    moed_l, morp_l_extm_vals, moed_l_asarr = warp(l, H_l_to_m)

    r = Image.open(path_r)
    moed_r, morp_r_extm_vals, moed_r_asarr = warp(r, H_r_to_m)

    m = Image.open(path_m)

    maxx = max(morp_l_extm_vals['maxx'], morp_r_extm_vals['maxx'], m.width)
    maxy = max(morp_l_extm_vals['maxy'], morp_r_extm_vals['maxy'], m.height)

    minx = min(morp_l_extm_vals['minx'], morp_r_extm_vals['minx'], m.width)
    miny = min(morp_l_extm_vals['miny'], morp_r_extm_vals['miny'], m.height)
    
    h = maxy-miny
    w = maxx-minx
    combined_im = np.zeros((w,h,3))

    # copy middle im
    combined_im[0-minx:-minx+m.width, 0-miny:-miny+m.height, :] = np.swapaxes(np.asarray(m),0,1)
    
    
    # combined_im[0:moed_l_asarr.shape[0], 0:moed_l_asarr.shape[1]]  = moed_l_asarr

    # combined_im[0-minx:-minx+m.width, 0-miny:-miny+m.height, :] = np.swapaxes(np.asarray(m),0,1)
    
    for i in range(moed_l_asarr.shape[0]):
        for j in range(moed_l_asarr.shape[1]):
            if np.sum(combined_im[i, j, :]) < np.sum(moed_l_asarr[i, j, :]):
                combined_im[i, j, :] = moed_l_asarr[i, j, :]
    
    for i in range(moed_r_asarr.shape[0]):
        for j in range(moed_r_asarr.shape[1]):
            if np.sum(moed_r_asarr[i, j, :]) != 0:
                if np.sum(moed_r_asarr[i, j, :]) > np.sum(combined_im[i+ w - moed_r_asarr.shape[0], j+ h -moed_r_asarr.shape[1], :]):   
                    combined_im[i+ w - moed_r_asarr.shape[0], j+ h -moed_r_asarr.shape[1], :] = moed_r_asarr[i, j, :]
    
                
    
    

    res = Image.fromarray(np.swapaxes(combined_im,0,1).astype('uint8')) # pillow expects hXw image, I had wXh
    
    left, top, right, bottom = 0, -miny, res.width-1, -miny+m.height # the image is not in standart coord sist. y axis is upside down
    cropped = res.crop((left, top, right, bottom))
    
    return res, cropped
    


# In[ ]:


res, res_crpd = merge_3_ims(building_paths['l1'],building_paths['m'],building_paths['r1'], n=5, save_points=False, load_points=False, title="choose 5 points")
plt.imshow(res)
plt.title('5 corr. points')
plt.show()


res, res_crpd = merge_3_ims(building_paths['l1'],building_paths['m'],building_paths['r1'], n=12, save_points=False, load_points=False, title="choose 12 points")
plt.imshow(res)
plt.title('12 corr. points')
plt.show()


res, res_crpd = merge_3_ims(building_paths['l1'],building_paths['m'],building_paths['r1'], n=12, save_points=False, load_points=False, normalize=False, title="choose 12 points 3 should be wrong")
plt.imshow(res)
plt.title('12 corr. points 3 were wrong not normalized')
plt.show()

res, res_crpd = merge_3_ims(building_paths['l1'],building_paths['m'],building_paths['r1'], n=12, save_points=False, load_points=False, normalize=True, title="choose 12 points 3 should be wrong")
plt.imshow(res)
plt.title('12 corr. points 3 were wrong')
plt.show()


res, res_crpd = merge_3_ims(building_paths['l1'],building_paths['m'],building_paths['r1'], n=12, save_points=False, load_points=False, normalize=True, title="choose 12 points 5 should be wrong")
plt.imshow(res)
plt.title('12 corr. points 5 were wrong')
plt.show()

res, res_crpd = merge_3_ims(building_paths['l1'],building_paths['m'],building_paths['r1'], n=12, save_points=False, load_points=False, title="choose 12 points i will add noise and normalize", noise_scale=16)
plt.imshow(res)
plt.title('12 corr. points added noise with stdev=16, normalized')
plt.show()

res, res_crpd = merge_3_ims(building_paths['l1'],building_paths['m'],building_paths['r1'], n=12, normalize=False, save_points=False, load_points=False, title="choose 12 points i will add noise, wont normalize", noise_scale=16)
plt.imshow(res)
plt.title('12 corr. points added noise with stdev=16, not normalized')
plt.show()


