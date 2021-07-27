import itertools
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats.stats import iqr, zscore
import itertools

idx = pd.IndexSlice
user_profile = os.environ['USERPROFILE']
user_desktop = user_profile + r"\Desktop\txt py"
bulan2 = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'Jun','07':'Jul','08':'Aug','09':'Sep','10':'Okt','11':'Nov','12':'Des'}
bulan1 = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Okt','Nov','Des']

def read_mdat(mdat):
    m_datas = []
    for dat in mdat :
        m_data = pd.read_csv(fr'{user_desktop}\{dat}.csv')
        m_data = m_data.set_index(['lokasi','nama_komoditas'])
        m_datas.append(m_data)
    m_datas1 = pd.concat(m_datas, axis=1, keys=bulan1).sort_index()
    #m_datas1 = m_datas1.resample('W').fillna(method='ffill')
    return m_datas1
    
class clean:
    def __init__(self, df):
        self.df = df
        self.cols = self.df.columns
    def rem_null(self):
        #mengganti 0 menjadi nan di setiap kolom dan membuang kolom dan baris yang kosong
        self.df[self.cols] = self.df[self.cols].replace({0 : np.nan})
        self.df = self.df.dropna(axis=1, how="all")
        self.df = self.df.dropna(axis=0, how="all")
        self.df = self.df.reset_index(level=0, drop=True)
        self.df = self.df.stack(level=1)
        self.df = self.df.fillna(method='ffill',axis=1).fillna(method='bfill')
        self.df.drop_duplicates(subset=bulan1, keep='first', inplace=True)
        self.df['Feb']['Bawang Putih']['2019-02-19'] = 21000
        self.plotting()
        return self.df

    def plotting(self):
        print(self.df.shape)
        columns = self.df.index.get_level_values(0).unique().tolist()
        s1 = []
        s2 = []
        for col in columns :
            for bul in bulan1 :
                s1.append(self.df[bul][col].drop_duplicates(keep="first").index.tolist())
                s2.append(self.df[bul][col].drop_duplicates(keep="first").values.tolist())
            s1_flat = list(itertools.chain(*s1))
            s2_flat = list(itertools.chain(*s2))
            xs, ys = zip(*sorted(zip(s1_flat, s2_flat)))
            xs = list(xs)
            ys = list(ys)
            print(f'tgl: {xs}, harga: {ys}\n')
            plt.plot(xs, ys)
            plt.xlim(0.5)
            plt.xlabel('Tanggal')
            plt.xticks(rotation=45)
            plt.ylabel('Harga')
            plt.title(f'Kenaikan Harga komoditas {col} tahun 2019')
            plt.show()
            s1.clear()
            s2.clear()
            s1_flat.clear()
            s2_flat.clear()
        
        
    
def plot_satu(nama_komoditas, bulan) :
    s1 = []
    s2 = []
    nama_komod = []
    list_harga_s = []
    list_all_komoditas = []
    for bul in bulan :
        list_harga = komoditas_bersih[bul].loc[idx[:,nama_komoditas,:]].values
        for l in list_harga :
            for t in l :
                list_harga_s.append(t)
        list_harga = pd.Series(list_harga_s).unique()
        print(len(list_harga))
        s2.append(list_harga)
        print(s2)
        nama_komod.append(komoditas)
        for i in list_harga:
            s1.append(bul)
        
        
    plt.plot((1,2,3,4,5,6,7,8,9,10,11,12), s2)
    plt.xlim(0, 10)
    plt.xlabel('Tanggal')
    plt.ylabel('Harga')
    for nama in nama_komod :
        plt.title(f'Kenaikan Harga komoditas {nama} bulan Januari 2019')
    plt.show()
    
#masukkan data csv
pasar_andir = ['pasar-andir-jan', 'pasar-andir-feb', 'pasar-andir-mar', 'pasar-andir-apr', 'pasar-andir-may', 'pasar-andir-jun', 'pasar-andir-jul', 'pasar-andir-aug', 'pasar-andir-sep', 'pasar-andir-okt', 'pasar-andir-nov', 'pasar-andir-des']
komoditas = read_mdat(pasar_andir)
komoditas_bersih = clean(komoditas)
komoditas_bersih = komoditas_bersih.rem_null()

#print(komoditas_bersih.head(10))
#print(komoditas_bersih.columns.dtype)

#instalasi untuk melihat curve kenaikan setiap komoditas
#nama_k = komoditas_bersih.reset_index(level=0, drop=True)
#list_nama_komoditas = nama_k.index.tolist()

#list_harga = komoditas_bersih['Jan'].loc[idx[:,'Bawang Merah',:]].columns
#list_harga = list(itertools.chain.from_iterable(list_harga))
#list_harga = pd.Series(list_harga)
#print(list_harga)
#for komoditas in list_nama_komoditas :
    #plot_satu([komoditas], bulan1)

    
#plot_satu('Bawang Merah', bulan1)




