import pandas as pd
import os
import numpy as np

user_profile = os.environ['USERPROFILE']
user_desktop = user_profile + r"\Desktop\txt py"

class data_bulan:
    def __init__(self, nama_data, col):
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
        self.df = self.df.dropna(axis=1, how="all")
        self.df = self.df.dropna(axis=0, how="all")
        self.df.drop(columns=["lokasi"], inplace=True, axis=1)
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
            a = self.df.loc[i].unique().tolist()
            b = int(a[-1]) - int(a[0])
            perb.append(b)
        self.df['Perbedaan_Harga_Awal/Akhir_Bulan'] = perb
        self.df['Perbedaan_Harga_Awal/Akhir_Bulan'] = self.df['Perbedaan_Harga_Awal/Akhir_Bulan'].replace({0:'stabil'})
        print(f'Perubahan Harga Komoditas {self.tgl} :')
        print(self.df['Perbedaan_Harga_Awal/Akhir_Bulan'])
        nama_file = input("\nsave data dengan nama\n(enter untuk save dengan file yang sama)\n(tulis |tidak| untuk tidak mengesave\nInput : )")
        if nama_file == '':
            self.df.to_csv(self.nama_data)
        elif nama_file.casefold() == 'tidak' :
            print('file tidak di save')
        else :
            print(f"file di save di {user_desktop}\{nama_file}.csv")
            self.df.to_csv(user_desktop + rf"\{nama_file}.csv")

#masukkan data csv
b_des = data_bulan(user_desktop + r"\pasar_andir.csv", ["nama_komoditas"])


#print csv
b_des.rem_null()