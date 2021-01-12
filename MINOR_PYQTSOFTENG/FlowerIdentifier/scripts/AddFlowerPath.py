import pymysql
import os

conn=pymysql.connect(host='localhost',user='root',password='toor',db='flower')
flowers=os.listdir(r"C:\Users\windows\Desktop\FlowerIdentifier\images")
masks=os.listdir(r"C:\Users\windows\Desktop\FlowerIdentifier\masks")

with conn.cursor() as curr:
    
    for item1,item2 in zip(flowers,masks):
        flowerid=item1.split('_')[2].split('.')[0]
        flowername=item1.split('_')[1]
        flowerpath=r"C:\Users\windows\Desktop\FlowerIdentifier\images"+"\\"+item1
        maskpath=r"C:\Users\windows\Desktop\FlowerIdentifier\masks"+"\\"+item2

        print(flowerid)
        print(flowername)
        print(flowerpath)
        print(maskpath)
        

        query='INSERT INTO flower.flowerpath(`Flower ID`, `Flower Name`, `Flower Image Path`,`Mask Image Path`) ' + \
              'VALUES(%s,%s,%s,%s);'
        curr.execute(query,(int(flowerid),flowername,flowerpath,maskpath))
        conn.commit()
