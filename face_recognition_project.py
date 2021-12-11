from rtree import index
import face_recognition
from pathlib import Path
import heapq
import glob
from queue import PriorityQueue
import numpy as np
""""
- Extracción de características 
- Indexación de vectores característicos para búsquedas eficientes
"""
p = index.Property()
p.dimension = 128 #D
p.buffering_capacity = 10 #M
Rtree = index.Index('RtreeLab', properties=p)

def fill_Rtree_with_encondings():
    i = 0
    encodings = read_encoding()
    for k in encodings:
        Rtree.insert(i, encodings[k], k)
        i= i+ 1
    return Rtree  

def build():
    write_encodings()
    Rtree = fill_Rtree_with_encondings()
    
def knn_search_rtree(k, image_name):
    image = face_recognition.load_image_file(image_name)
    Q = face_recognition.face_encodings(image)[0]
    return list(Rtree.nearest(list(Q), k, 'raw'))

def range_search(r, image_name):
    images = read_encoding()
    image = face_recognition.load_image_file(image_name)
    image_encoding = face_recognition.face_encodings(image)[0]
    image_encoding = [image_encoding]
    result = []
    for i in images:
        if len(images[i])>0:
            image_compare_encoding = images[i]
            dist = face_recognition.face_distance(np.array(image_encoding), np.array(image_compare_encoding))
            if dist < r:
                result.append(i)
    return result

def knn_search(k, image_name):
    images = read_encoding()
    image = face_recognition.load_image_file(image_name)
    image_encoding = face_recognition.face_encodings(image)[0]
    image_encoding = [image_encoding]
    result = PriorityQueue()
    for i in images:
        if len(images[i])>0:
            image_compare_encoding = images[i]
            dist = face_recognition.face_distance(np.array(image_encoding), np.array(image_compare_encoding))
            result.put((dist, i))
    result_final = []
    for i in range(k):
        result_final.append(result.get()[1])
    return result_final

def read_encoding():
    dic = {}
    with open('encodings.txt', 'r') as f:
        for i in f.readlines():
            algo = i.split(',')
            lista = []
            for j in algo[1:len(algo)-1]:   
                lista.append(float(j))
            dic[algo[0]] = lista
    return dic

def write_encodings():
    images = glob.glob("static\\lfw\\lfw\\*\\*")
    images = images[:100]
    with open('encodings.txt', 'a') as f:   
        for i in images:
            image = face_recognition.load_image_file(i)           
            if len(face_recognition.face_encodings(image))>0:
                image_encoding = face_recognition.face_encodings(image)[0]              
                #f.write(i.split('\\')[7] + ',')
                f.write(i + ',')
                for j in image_encoding:
                    f.write(str(j)+',')
                f.write('\n')

build()           
#print(range_search(0.01, 'C:\\Users\\lojaz\\Desktop\\BD2_Proyecto3\\lfw\\lfw\\Abba_Eban\\Abba_Eban_0001.jpg'))