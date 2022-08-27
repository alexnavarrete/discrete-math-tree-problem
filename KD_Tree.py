import osgeo.ogr
import math
class Node:pass

# Function that calculates the distance between two cities, given their latitude and longitude.
def haversine_distance((lat1,lon1),(lat2,lon2)):  #distancia entre dos ciudades
    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) / math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return 6371 * c
    
# Function to display the kdtree as a tree.
def kdtree_create_view(kdtree,arbol):
    if not kdtree:
        arbol.pop()
        return None
    else:
        print(arbol,kdtree.Name,kdtree.localizacion)
        arbol.append(1)
        kdtree_create_view(kdtree.hijoizquierdo,arbol)
        arbol.append(2)
        kdtree_create_view(kdtree.hijoderecho,arbol)
        arbol.pop()
    return None
    
#--------ENLIST-----------------
def crear_lista(kdtree,point,dis,nombre):
    if not kdtree:
        return None
    else:
        dis.append(haversine_distance((point),(kdtree.localizacion)))
        nombre.append(kdtree.Name)
        crear_lista(kdtree.hijoizquierdo,point,dis,nombre)
        crear_lista(kdtree.hijoderecho,point,dis,nombre)
    return None
    
# Sort the list of names and distances. (bubblesort)
def ordenar_lista(Distancias,nombres):
    cont=0
    while cont<(len(Distancias)-1):
        for j in range(0,len(Distancias)-1):
            if(Distancias[j]>Distancias[j+1]):
                aux_distancia = Distancias[j]
                aux_NOMBRE = nombres[j]
                Distancias[j] = Distancias[j+1]
                nombres[j] = nombres[j+1]
                Distancias[j+1]= aux_distancia
                nombres[j+1] = aux_NOMBRE
        cont+=1
    return None
    
# Sort to find midpoints to perform splits on the kdtree.
def shellsort(pointlist,names,ax):
    N=int(len(pointlist))
    salto=int(N/2)
    array=pointlist[:]
    #------SHELL SORT-----Longitude
    if(ax==1):
        salto=0
        salto+=int(N/2)
        while salto!=0:
            cambios=1
            while cambios!=0 :
                cambios=0;
                i=salto
                while  i<N:
                    if array[i-salto][0] > array[i][0]:
                        Name=names[i]
                        aux=array[i]
                        names[i]=names[i-salto]
                        array[i]=array[i-salto]
                        array[i-salto]=aux
                        names[i-salto]=Name
                        cambios+=1
                    i+=1
            salto/=2
    
    #------------SHELL SORT--------Latitude
    if(ax==-1):
        salto=int(0)
        salto+=int(N/2)
        i=int(0)
        while salto!=0:
            cambios=1
            while cambios!=0 :
                cambios=0;
                i=salto
                while  i<N:
                    if array[i-salto][1] > array[i][1]:
                        Name=names[i]
                        aux=array[i]
                        names[i]=names[i-salto]
                        array[i]=array[i-salto]
                        array[i-salto]=aux
                        names[i-salto]=Name
                        cambios+=1
                    i+=1
            salto/=2
    pointlist=array
    #--------transfer to new order
    fin=[]
    fin.append(pointlist)
    fin.append(names)
    return fin 
    
# We create the kdtree.
def kdtree_create(pointlist,names,axis,depth=0):
    #Return node and sub-trees
    axis=axis*(-1)
    if not pointlist:
        
        return None
    #--------------------------------------------------------------------------
    fin=shellsort(pointlist,names,axis)
    pointlist=fin[0]
    names=fin[1]
    #print(pointlist)
    #print(names)
    median = len(pointlist)/2
    #--------------------------------------------------------------------------
    node=Node()    
    node.localizacion= pointlist[median]
    node.Name=names[median]
    #print node.Name
    node.hijoizquierdo= kdtree_create(pointlist[0:median],names[0:median],depth+1,axis)
    node.hijoderecho= kdtree_create(pointlist[median+1:],names[median+1:], depth+1,axis)    
    return node     
       
# Function for the "n" closest cities.
def kdtree_knn(kdtree,point,n):
    Distancias = []
    nombre= []
    crear_lista(kdtree,point,Distancias,nombre)
    ordenar_lista(Distancias,nombre)
    i=0
    while i<n+1:
        if(Distancias[i]!=0):
            print(Distancias[i],nombre[i])
        i+=1
    return None
    #return zip(Distancias[:n+1],nombre[:n+1])
    
# Funcion para las ciudades dentro de rango "n".
def kdtree_Range(kdtree,point,n):
    Distancias = []
    nombre= []
    crear_lista(kdtree,point,Distancias,nombre)
    ordenar_lista(Distancias,nombre)
    cantidad=len(nombre)
    i=0
    while i<cantidad:
        if((Distancias[i]<n) and (Distancias[i])>0):
            print(Distancias[i],nombre[i])
        i+=1
    return None
    #return zip(Distancias[],nombre[])

#-----------------------------------TERMINO FUNCIONES--------------------------------------------------------------------



#MAIN()
#----Read data with OSGEO library.
ciudades={}
shapefile=osgeo.ogr.Open("cl_ciudades_geo.shp")
layer=shapefile.GetLayer(0)
spatialRef=layer.GetSpatialRef().ExportToProj4()
numFeatures=layer.GetFeatureCount()

#----Extract data to variables.
for i in range(numFeatures):
    feature=layer.GetFeature(i)
    geometry=feature.GetGeometryRef()
    point=geometry.GetPoint(0)
    ciudades[feature.items()['NOMBRE']]=(point[1],point[0])
#----------------------------------------------------------------------------

# Create from the KDTREE tree.
kdtree=kdtree_create(ciudades.values(),ciudades.keys(),-1)
#PRUEBAS FUNCIONES
#kdtree_Range(kdtree,(-34.408604, -70.857844),15)
#kdtree_knn(kdtree,(-34.408604, -70.857844),10)