from rtree import index
import face_recognition
from pathlib import Path


""""
- Extracción de características 
- Indexación de vectores característicos para búsquedas eficientes
"""

def get_encodings():
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
                    print(face_recognition)
                    for faceEncoding in facesEncoding:
                        listAux = list(faceEncoding)
                        for cord in faceEncoding:
                            listAux.append(cord)
                        Rtree.insert(i, listAux, ( path +  str(name) + '\\' + str(item.name) ))
                        final_encodings.append(listAux)
                        i= i+ 1
    Rtree.close()
    return final_encodings  





