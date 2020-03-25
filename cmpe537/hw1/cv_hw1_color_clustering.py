
# coding: utf-8

# In[1]:


import matplotlib
matplotlib.use('TkAgg')


from PIL import Image
from matplotlib import pyplot as plt
import numpy as np
                    


# In[2]:


class Cluster:
    def __init__(self,centroid):
        self.centroid = centroid
        self.r_total = 0
        self.g_total = 0
        self.b_total = 0
        self.size = 0
        
    def add(self, pixel):
        self.r_total+=pixel.rgb[0]
        self.g_total+=pixel.rgb[1]
        self.b_total+=pixel.rgb[2]
        self.size+=1
    
    def reset_points(self):
        self.size=0
        self.r_total=0
        self.g_total=0
        self.b_total=0
    
    def update_centroid(self):
        if self.size != 0:
            r = self.r_total/self.size
            g = self.g_total/self.size
            b = self.b_total/self.size
            self.centroid.rgb = (r,g,b)

class Pixel():
    
    def __init__(self,koordinates,rgb):
        self.koordinates = koordinates
        self.rgb = rgb
    
    def __hash__(self):
        return hash(self.koordinates)
    
    def __eq__(self,other):
        return self.koordinates == other.koordinates

# In[3]:


def click_select(img, n):
    plt.imshow(img)
    points = plt.ginput(n, show_clicks=True)
    return points

def random_select(img, n):
    width, height = img.size
    return [(np.random.uniform(0,width),np.random.uniform(0,height)) for _ in range(n)]

def distance(centroid, pixel):
    return sum((centroid.rgb[i]-pixel.rgb[i])**2 for i in range(3))


def quantize(img, K, inits, limit):
    assert K == len(inits)
    clusters = [Cluster(Pixel(inits[i],img.getpixel(inits[i]))) for i in range(K)]
    width, height = img.size
    ic = 0
    pixel_map = dict()
    converged = False
    while ic < limit and not converged:
        converged = True # hopefully
        for cluster in clusters:
            cluster.update_centroid()
            cluster.reset_points()
            
        for i in range(width):
            for j in range(height):
                rgb = img.getpixel((i,j))
                pixel = Pixel((i,j),rgb)
                prev_cluster = pixel_map.get(pixel,None)
                min_dist = float("inf")
                chosen_cluster = None
                for cluster in clusters:
                    if distance(cluster.centroid, pixel) < min_dist:
                        min_dist = distance(cluster.centroid, pixel)
                        chosen_cluster = cluster
                
                chosen_cluster.add(pixel)
                pixel_map[pixel] = chosen_cluster
                if chosen_cluster is not prev_cluster:
                    converged = False
                    
        ic+=1

    if converged:
        print("Converged at iteration: " + str(ic))
    else:
        print("Iteration limit reached!")
    return clusters, pixel_map

# In[ ]:

iteration_limit = 10

automized = False
bonus = True

if not automized and not bonus:
    image_path = "3.jpg"

    with open(image_path, 'rb') as f:
        img = Image.open(f).convert('RGB')
        img.load()

    all_points = []
    width, height = img.size
    for K in [2,4,8,16,32]:
        new_points = click_select(img, K)
        all_points.append(new_points)
    
    width, height = img.size

    for points in all_points:
        K = len(points)
        clusters, pixel_map = quantize(img, K, points,iteration_limit)


        new_img = image = Image.new('RGB', (width, height))
        for pixel,cluster in pixel_map.items():
            new_img.putpixel(pixel.koordinates,tuple(int(x) for x in cluster.centroid.rgb))

        new_img.save(image_path + 'handpickedinits_' + str(K) + '_colors_'+ str(iteration_limit) + '_iters.jpg')
        print(image_path,K,'done')


elif not bonus:
    for image_path in ["1.jpg","2.jpg","3.jpg"]:
        with open(image_path, 'rb') as f:
            img = Image.open(f).convert('RGB')
            img.load()

        width, height = img.size

        for K in [2,4,8,16,32]:

            points = random_select(img, K)

            clusters, pixel_map = quantize(img, K, points,iteration_limit)

            new_img = image = Image.new('RGB', (width, height))
            for pixel,cluster in pixel_map.items():
                new_img.putpixel(pixel.koordinates,tuple(int(x) for x in cluster.centroid.rgb))

            new_img.save(image_path + '_' + str(K) + '_colors_'+ str(iteration_limit) + '_iters.jpg')
            print(image_path, K, 'complete!')


if bonus:
    import cv2
    from collections import Counter
    import matplotlib.pyplot as plt
    image_path = '3.jpg'
    image = cv2.imread(image_path)
    import numpy as np
    
    K = 3
    iteration_limit = 10
    limit = 3
    hist = cv2.calcHist([image], [0, 1, 2],None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
    print("3D histogram shape: %s, with %d values" % (hist.shape, hist.flatten().shape[0]))
    c = Counter()
    for i in range(8):
        for j in range(8):
            for k in range(8):
                c[(i,j,k)] = hist[i,j,k]

    points = [(r*32+16, g*32+16, b*32+16) for ((b,g,r),_) in c.most_common(K)]

    clusters = [Cluster(Pixel(None,points[i])) for i in range(K)]
    img = Image.fromarray(image)
    width, height = img.size
    ic = 0
    pixel_map = dict()
    converged = False
    
    while ic < limit and not converged:
        converged = True # hopefully
        for cluster in clusters:
            cluster.update_centroid()
            cluster.reset_points()
            
        for i in range(width):
            for j in range(height):
                rgb = img.getpixel((i,j))
                pixel = Pixel((i,j),rgb)
                prev_cluster = pixel_map.get(pixel,None)
                min_dist = float("inf")
                chosen_cluster = None
                for cluster in clusters:
                    if distance(cluster.centroid, pixel) < min_dist:
                        min_dist = distance(cluster.centroid, pixel)
                        chosen_cluster = cluster
                
                chosen_cluster.add(pixel)
                pixel_map[pixel] = chosen_cluster
                if chosen_cluster is not prev_cluster:
                    converged = False
                    
        ic+=1

    new_img = image = Image.new('RGB', (width, height))
    for pixel,cluster in pixel_map.items():
        new_img.putpixel(pixel.koordinates,tuple(int(x) for x in cluster.centroid.rgb))

    new_img.save(image_path + '_bonus_' + str(K) + '_colors_'+ str(iteration_limit) + '_iters.jpg')
    print(image_path, K, 'complete!')