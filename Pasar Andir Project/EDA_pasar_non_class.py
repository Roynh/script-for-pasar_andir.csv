import pandas as pd
import os
import numpy as np

user_profile = os.environ['USERPROFILE']
user_desktop = user_profile + r"\Desktop\txt py"
#Read data 
df = pd.read_csv(user_desktop + r"\pasar_andir.csv", index_col=["nama_komoditas"])
#Ganti 0 menjadi nan di setiap kolom
cols = []
for column in df.columns :
    cols.append(column)
df[cols] = df[cols].replace({0 : np.nan})
#Buang kolom dan baris yang kosong
df = df.dropna(axis=1, how="all")
df = df.dropna(axis=0, how="all")
df.drop(columns=["lokasi"], inplace=True, axis=1)
#Mencari nilai null dan mengganti dengan unknown
cols.clear()
for column in df.columns :
    cols.append(column)
def cek_null(do=True) :
    if do == True :
        print(df.info())
        print(df.isnull().values.any())
cek_null(False)
df[cols] = df[cols].fillna('unknown')
cek_null(False)
#Analisi data secara deskriptif
#Membuat kolom perbedaan harga bulan di awal bulan dan akhir bulan
def perbedaan(frame) :
    df[cols] = df[cols].replace({'unknown':0})
    a = df.loc[frame].unique().tolist()
    b = int(a[-1]) - int(a[0])
    return b    
index = df.index.tolist()
a=[]
for i in index :
    a.append(perbedaan(i))
df['Perbedaan_Harga_Awal/Akhir_Bulan'] = a
#Kesimpulan
df['Perbedaan_Harga_Awal/Akhir_Bulan'] = df['Perbedaan_Harga_Awal/Akhir_Bulan'].replace({0:'stabil'})
print('Perubahan Harga Komoditas Bulan Desember 2019 : \n', df['Perbedaan_Harga_Awal/Akhir_Bulan'])
print(df.shape)