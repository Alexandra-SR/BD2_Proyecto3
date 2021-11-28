from rtree import index
import face_recognition
from pathlib import Path
import heapq

""""
- Extracción de características 
- Indexación de vectores característicos para búsquedas eficientes
"""

def fill_Rtree_with_encondings():
    p = index.Property()
    p.dimension = 128 #D
    p.buffering_capacity = 10 #M
    Rtree = index.Index('RtreeLab', properties=p)
    i = 0
    final_encodings=[]
    path = "lfw\lfw\\"
    basepath = Path(path)
    for entry in basepath.iterdir():
        if entry.is_dir():
            name = entry.name
            files = Path(path + str(name))
            files_in_basepath = files.iterdir()
            for item in files_in_basepath:
                if item.is_file():
                    image = face_recognition.load_image_file(item)
                    facesEncoding = face_recognition.face_encodings(image)
                    for faceEncoding in facesEncoding:
                        listAux = list(faceEncoding)
                        for cord in faceEncoding:
                            listAux.append(cord)
                        Rtree.insert(i, listAux, ( path +  str(name) + '\\' + str(item.name) ))
                        final_encodings.append(listAux)
                        i= i+ 1
    return Rtree  


def knn_search_sequential_pq(k, Q, n):  
    aux = 0  
    route = []
    faces = []
    path = "lfw\lfw\\"
    basepath = Path(path)
    for entry in basepath.iterdir():
        if entry.is_dir():
            name = entry.name
            files = Path(path + str(name))
            files_in_basepath = files.iterdir()
            for item in files_in_basepath:
                    image_name = path + str(name) + item.name
                    image = face_recognition.load_image_file(item)
                    facesEncoding = face_recognition.face_encodings(image)                    
                    for faceEncoding in facesEncoding:
                        if aux == n:
                            dist = face_recognition.face_distance(faces, Q)
                            auxArr = []
                            for i in range(0, aux, 1):
                                auxArr.append((dist[i], route[i]))
                            heapq.heapify(auxArr)    
                            return heapq.nsmallest(k, auxArr)
                        faces.append(faceEncoding)  
                        route.append(image_name)
                        aux += 1
    dist = face_recognition.face_distance(faces, Q)
    auxArr = [] 
    for i in range(0, aux, 1):
        auxArr.append((dist[i], route[i]))
    heapq.heapify(auxArr)    
    return heapq.nsmallest(k, auxArr)


def knn_search_rtree(k, Q):
    Rtree = fill_Rtree_with_encondings()
    coordinatesListQuery = list(Q)
    for i in Q:
        coordinatesListQuery.append(i)
    return list(Rtree.nearest(coordinatesListQuery, k, 'raw'))


