from os.path import join
import pandas as pd



def read_folds(k,   path, root_path):
    assert k>0, 'Number of folds to read must be greater than 0, obviously'
    assert k<11, 'There are only 10 folds avaliable'
    limit = k*600
    same_pairs = []
    different_pairs = []
    for count, line in enumerate(open(path,'r')):
        if count == limit: break
        if (count // 300) % 2 == 0:
            name, id1, id2 = line.split('\t')
            path1 = join(root_path,name, '{}_{:04d}.jpg'.format(name, int(id1)))
            path2 = join(root_path,name, '{}_{:04d}.jpg'.format(name, int(id2)))
            same_pairs.append((path1, path2, name, name))

        else:
            name1, id1, name2, id2 = line.split('\t')
            path1 = join(root_path,name1, '{}_{:04d}.jpg'.format(name1, int(id1)))
            path2 = join(root_path,name2, '{}_{:04d}.jpg'.format(name2, int(id2)))
            different_pairs.append((path1, path2, name1, name2))
    
    return same_pairs, different_pairs

def people_with_at_least_n_images(limit, path):
    names = []
    numbers = []
    with open(path) as f:
        for line in f:
            try:
                name, num = line.split('\t')
                num = int(num)
            except:
                continue
            if num >= limit:
                names.append(name)
                numbers.append(num)
    return pd.DataFrame({'name' : names,'image_num' : numbers})

def load_names(path, lower_limit=0, upper_limit=float('Inf')):
    names = []
    numbers = []
    with open(path) as f:
        for line in f:
            try:
                name, num = line.split('\t')
                num = int(num)
            except:
                continue
            if upper_limit >= num >= lower_limit:
                for i in range(1,num+1):
                    names.append(name)
                    numbers.append(i)
    return pd.DataFrame({'name' : names,'image_num' : numbers})
