from warnings import warn

import dlib

def face_closeup(detector, img, margin=0, method='hog'):
    if method == 'hog':
        faceRects = detector(img, 0)
        if len(faceRects) < 1:
            raise ValueError('Could not find any faces.')
        elif len(faceRects) > 1:
            warn('Found {} faces, using the most central one'.format(len(faceRects)))
            
            h, w = img.shape
            best = 0
            best_distance = 1000
            for i in range(len(faceRects)):
                x1 = faceRects[i].left() - margin
                y1 = faceRects[i].top() - margin
                x2 = faceRects[i].right() + margin
                y2 = faceRects[i].bottom() + margin
                x = (x1+x2)/2
                y = (y1+y2)/2
                dist = (h/2 - x)**2 + (w/2 - y)**2
                if dist < best_distance:
                    best_distance = dist
                    best = i
            x1 = faceRects[best].left() - margin
            y1 = faceRects[best].top() - margin
            x2 = faceRects[best].right() + margin
            y2 = faceRects[best].bottom() + margin
        else:
            x1 = faceRects[0].left() - margin
            y1 = faceRects[0].top() - margin
            x2 = faceRects[0].right() + margin
            y2 = faceRects[0].bottom() + margin
    
    elif method == 'cnn':
        dets = detector(img, 0)
        if len(dets) < 1:
            raise ValueError('Could not find any faces.')
        elif len(dets) > 1:
            warn('Found {} faces, using the one with the highest confidence score.'.format(len(dets)))
            best = 0
            best_score = -999
            for i in range(len(dets)):
                if dets[i].confidence > best_score:
                    best = i
                    best_score = dets[i].confidence
            
            x1 = dets[best].rect.left() - margin
            y1 = dets[best].rect.top() - margin
            x2 = dets[best].rect.right() + margin
            y2 = dets[best].rect.bottom() + margin
                
        else:
            x1 = dets[0].rect.left() - margin
            y1 = dets[0].rect.top() - margin
            x2 = dets[0].rect.right() + margin
            y2 = dets[0].rect.bottom() + margin
    
    else:
        raise ValueError('unknown method: {}'.format(method))
    
    return img[x1:x2,y1:y2]


def cropped_and_aligned(img, detector, shape_predictor,size=224, method='hog'):
    if method == 'hog':
        faceRects = detector(img, 0)
        if len(faceRects) < 1:
            raise ValueError('Could not find any faces.')
        elif len(faceRects) > 1:
            warn('Found {} faces, using the most central one'.format(len(faceRects)))
            
            h, w ,d = img.shape
            best = 0
            best_distance = 1000
            for i in range(len(faceRects)):
                x1 = faceRects[i].left()
                y1 = faceRects[i].top()
                x2 = faceRects[i].right()
                y2 = faceRects[i].bottom()
                x = (x1+x2)/2
                y = (y1+y2)/2
                dist = (h/2 - x)**2 + (w/2 - y)**2
                if dist < best_distance:
                    best_distance = dist
                    best = i

            rect = faceRects[best]
        else:
            rect = faceRects[0]
    
    elif method == 'cnn':
        dets = detector(img, 0)
        if len(dets) < 1:
            raise ValueError('Could not find any faces.')
        elif len(dets) > 1:
            warn('Found {} faces, using the one with the highest confidence score.'.format(len(dets)))
            best = 0
            best_score = -999
            for i in range(len(dets)):
                if dets[i].confidence > best_score:
                    best = i
                    best_score = dets[i].confidence
            
            rect = dets[best].rect
                
        else:
            rect = dets[0].rect

    
    else:
        raise ValueError('unknown method: {}'.format(method))

    detection = rect
    image = dlib.get_face_chip(img, shape_predictor(img, detection), size=size)
    return image