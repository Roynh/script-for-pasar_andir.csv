import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

user_profile = os.environ['USERPROFILE']
user_desktop = user_profile + r"\Desktop\txt py"
bulan = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Okt','Nov','Des']
bulan1 = []
for bul in bulan :
    bulan1.append(bul.lower())

idx = pd.IndexSlice
try :
    os.makedirs(user_profile)
    print('Folder txt py dibuat !')
except FileExistsError:
    None

class data_bulan:
    def __init__(self, nama_data, col='nama_komoditas'):
        self.nama_data = nama_data
        self.col = col
        self.df = pd.read_csv(self.nama_data, index_col= self.col)
        index_a = self.df.columns.to_list()
        self.tgl = index_a[1]+ " - " + index_a[-1]
    def rem_null(self):
        #Ganti 0 menjadi nan di setiap kolom
        cols = []
        for column in self.df.columns :
            cols.append(column)
        self.df[cols] = self.df[cols].replace({0 : np.nan})
        self.df = self.df.drop(columns=['lokasi'], axis=1)
        self.df = self.df.dropna(axis=1, how="all")
        self.df = self.df.dropna(axis=0, how="all")
        #Mencari nilai null dan mengganti dengan unknown
        cols.clear()
        for column in self.df.columns :
            cols.append(column)
        self.df[cols] = self.df[cols].fillna('unknown')
        self.df[cols] = self.df[cols].replace({'unknown':0})
        self.perbedaan()
        #Analisi data secara deskriptif
    def perbedaan(self) :
        perb =[]
        index_a = self.df.index.tolist()
        for i in index_a :
            a = self.df.loc[i].tolist()
            b = int(a[-1]) - int(a[0])
            perb.append(b)
        self.df['perbedaan_harga'] = perb
        self.df['perbedaan_harga'] = self.df['perbedaan_harga'].replace({0:'stabil'})
    def stats(self) :
        percent =[]
        df_percent = self.df.drop('perbedaan_harga', 1)
        index_a = df_percent.index.tolist()
        for (i, perb) in zip(index_a, self.df['perbedaan_harga'].replace({'stabil':0}).tolist()) :
            a = df_percent.loc[i].tolist()
            b = (perb/int(a[0]))
            c = "{:.0%}".format(b)
            percent.append(c)
        self.df['percent_kenaikan'] = percent
        #df_perb.reset_index(inplace=True)
        #print(df_perb.dtypes)
        #df_perb.plot.bar('nama_komoditas','perbedaan_harga')
        return self.df
        
data_jan = data_bulan(user_desktop + r'\pasar-andir-jan.csv')
data_jul = data_bulan(user_desktop + r'\pasar-andir-jul.csv')
data_aug = data_bulan(user_desktop + r'\pasar-andir-aug.csv')
data_des = data_bulan(user_desktop + r'\pasar-andir-des.csv')

data_jan.rem_null()
data_jul.rem_null()
data_aug.rem_null()
data_des.rem_null()

jan = data_jan.stats()
jul = data_jul.stats()
aug = data_aug.stats()
des = data_des.stats()

    
#print csv
data_full = pd.concat([jan,jul,aug,des], axis=1, keys=['jan','jul','aug','des'])
data_full.to_csv(user_desktop + r'\data_full.csv')
#data_campur = pd.concat([data_aug,data_des],axis=1, keys=['Aug','Des'])
print(data_full.head(15))
#data_campur.plot.bar('nama_komoditas', data_campur_stack['Aug'])
