
import pandas as pd
#gorev1
#Soru 1: persona.csv dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz
persona = pd.read_csv("persona.csv")
df = persona.copy()

def check_df(dataframe, head=5):
    print("##################### Shape #####################")
    print(dataframe.shape)
    print("##################### Types #####################")
    print(dataframe.dtypes)
    print("##################### info #####################")
    print(dataframe.info())
    print("##################### Head #####################")
    print(dataframe.head(head))
    print("##################### Tail #####################")
    print(dataframe.tail(head))
    print("##################### NA #####################")
    print(dataframe.isnull().sum())
    print("##################### Quantiles #####################")
    print(dataframe.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
    print("##################### NA #####################")
    print(dataframe.isnull().sum())

check_df(df)

#Soru 2: Kaç unique SOURCE vardır? Frekansları nedir?
df["SOURCE"].nunique()

#soru 3 Kaç unique PRICE vardır?
df["PRICE"].nunique()

#Soru 4: Hangi PRICE'dan kaçar tane satış gerçekleşmiş?
df["PRICE"].value_counts()

#Soru 5: Hangi ülkeden kaçar tane satış olmuş?
df.groupby("COUNTRY").agg({"PRICE": "count"})

#Soru 6: Ülkelere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("COUNTRY").agg({"PRICE": "sum"})

#Soru 7: SOURCE türlerine göre satış sayıları nedir?
df.groupby("SOURCE").agg({"PRICE": "count"})

#Soru 8: Ülkelere göre PRICE ortalamaları nedir?
df.groupby("COUNTRY").agg({"PRICE": "mean"})

#Soru 9: SOURCE'lara göre PRICE ortalamaları nedir?
df.groupby("SOURCE").agg({"PRICE": "mean"})

#Soru 10: COUNTRY-SOURCE kırılımında PRICE ortalamaları nedir?

df.groupby(["COUNTRY", "SOURCE"]).agg({"PRICE": "mean"})

#gorev 2-3 :COUNTRY, SOURCE, SEX, AGE kırılımında ortalama kazançlar nedir?
# Çıktıyı PRICE’a göre sıralayınız.
#Önceki sorudaki çıktıyı daha iyi görebilmek için sort_values metodunu azalan olacak şekilde PRICE’a göre uygulayınız.
#Çıktıyı agg_df olarak kaydediniz.
agg_df = pd.DataFrame(df.groupby(["COUNTRY", "SOURCE", "SEX", "AGE"]).agg({"PRICE": "mean"}))
agg_df.sort_values("PRICE", ascending=False, inplace=True)
agg_df.head()

#gorev4: Index’te yer alan isimleri değişken ismine çeviriniz.
agg_df.reset_index(inplace=True)
agg_df.head()

#gorev5: age değişkenini kategorik değişkene çeviriniz ve agg_df’e ekleyiniz.

agg_df["AGE_CAT"] = pd.cut(agg_df["AGE"], [0, 18, 23, 30, 40, agg_df["AGE"].max()], labels=["0_18", "19_23", "24_30", "31_40", "41+"])
agg_df.tail()
agg_df.head()

#gorev6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız ve veri setine değişken olarak ekleyiniz.
#         Yeni eklenecek değişkenin adı: customers_level_based
agg_df["customer_level_based"] = [row[0].upper()+"_"+row[1].upper()+"_"+row[2].upper()+"_"+str(row[5]).upper() for row in agg_df.values]

#gorev7: Yeni müşterileri (personaları) PRICE'a göre 4 segmente ayırınız.
#Segmentleri SEGMENT isimlendirmesi ile değişken olarak agg_df’e ekleyiniz
agg_df["SEGMENT"] = pd.qcut(agg_df["PRICE"], 4, ["D", "C", "B", "A"])
agg_df.head()

#Segmentleri betimleyiniz.
agg_df.groupby(["SEGMENT"]).agg({"PRICE": ["mean", "max", "sum"]}).round(2)

#C segmentini analiz ediniz
segment_c = agg_df[agg_df["SEGMENT"] == "C"]
check_df(segment_c)

#customer level based-price dataframe i olusturunuz
clb_df = agg_df[["customer_level_based", "PRICE", "SEGMENT"]]

clb_df = clb_df.groupby("customer_level_based").agg({"PRICE": "mean"})

clb_df.head()

new_user1 = "TUR_ANDROID_FEMALE_31_40"
new_user2 = "FRA_IOS_FEMALE_31_40"

#alternatif 1 : reset_index() gerekmez. loc yardımı ile index sorgusu atılabilir
print("**new_user1**\n", clb_df.loc[new_user1])
print("**new_user2**\n", clb_df.loc[new_user2])

#alternatif 2
clb_df.reset_index(inplace=True)
print(clb_df[clb_df["customer_level_based"] == new_user1])

print(clb_df[clb_df["customer_level_based"] == new_user2])