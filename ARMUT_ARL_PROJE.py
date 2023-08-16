
#########################
# İş Problemi
#########################

# Türkiye’nin en büyük online hizmet platformu olan Armut, hizmet verenler ile hizmet almak isteyenleri buluşturmaktadır.
# Bilgisayarın veya akıllı telefonunun üzerinden birkaç dokunuşla temizlik, tadilat, nakliyat gibi hizmetlere kolayca
# ulaşılmasını sağlamaktadır.
# Hizmet alan kullanıcıları ve bu kullanıcıların almış oldukları servis ve kategorileri içeren veri setini kullanarak
# Association Rule Learning ile ürün tavsiye sistemi oluşturulmak istenmektedir.


#########################
# Veri Seti
#########################
#Veri seti müşterilerin aldıkları servislerden ve bu servislerin kategorilerinden oluşmaktadır.
# Alınan her hizmetin tarih ve saat bilgisini içermektedir.

# UserId: Müşteri numarası
# ServiceId: Her kategoriye ait anonimleştirilmiş servislerdir. (Örnek : Temizlik kategorisi altında koltuk yıkama servisi)
# Bir ServiceId farklı kategoriler altında bulanabilir ve farklı kategoriler altında farklı servisleri ifade eder.
# (Örnek: CategoryId’si 7 ServiceId’si 4 olan hizmet petek temizliği iken CategoryId’si 2 ServiceId’si 4 olan hizmet mobilya montaj)
# CategoryId: Anonimleştirilmiş kategorilerdir. (Örnek : Temizlik, nakliyat, tadilat kategorisi)
# CreateDate: Hizmetin satın alındığı tarih

import pandas as pd
pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
pd.set_option('display.width', 500)
# çıktının tek bir satırda olmasını sağlar.
pd.set_option('display.expand_frame_repr', False)
from mlxtend.frequent_patterns import apriori, association_rules



#########################
# GÖREV 1: Veriyi Hazırlama
#########################

# Adım 1: armut_data.csv dosyasınız okutunuz.

df = pd.read_csv("RecommendationSystems/datasets/armut_data.csv")
df.head()
df.info()
df.describe().T
df.isnull().sum()
# Adım 2: ServisID her bir CategoryID özelinde farklı bir hizmeti temsil etmektedir.
# ServiceID ve CategoryID'yi "_" ile birleştirerek hizmetleri temsil edecek yeni bir değişken oluşturunuz.

df["Hizmet"] = df["ServiceId"].astype(str) + "_" + df["CategoryId"].astype(str)
df.head()

# Adım 3: Veri seti hizmetlerin alındığı tarih ve saatten oluşmaktadır, herhangi bir sepet tanımı (fatura vb. ) bulunmamaktadır.

import datetime as dt

# Association Rule Learning uygulayabilmek için bir sepet (fatura vb.) tanımı oluşturulması gerekmektedir.
# Burada sepet tanımı her bir müşterinin aylık aldığı hizmetlerdir. Örneğin; 7256 id'li müşteri 2017'in 8.ayında aldığı 9_4, 46_4 hizmetleri bir sepeti;
# 2017’in 10.ayında aldığı  9_4, 38_4  hizmetleri başka bir sepeti ifade etmektedir. Sepetleri unique bir ID ile tanımlanması gerekmektedir.
# Bunun için öncelikle sadece yıl ve ay içeren yeni bir date değişkeni oluşturunuz. UserID ve yeni oluşturduğunuz date değişkenini "_"
# ile birleştirirek ID adında yeni bir değişkene atayınız.

df["CreateDate"] = pd.to_datetime(df["CreateDate"])

df["SepetID"] = df["UserId"].astype(str) + "_" + df["CreateDate"].dt.to_period(freq="M").astype(str)

df.head()

#########################
# GÖREV 2: Birliktelik Kuralları Üretiniz
#########################

# Adım 1: Aşağıdaki gibi sepet hizmet pivot table’i oluşturunuz.

df.pivot_table(columns=["Hizmet"], index=["SepetID"], values=["ServiceId"], aggfunc="count").head()
df.pivot_table(columns=["Hizmet"], index=["SepetID"], values=["ServiceId"], aggfunc="count").shape #(71220, 50)

#NaN yazan yerlere 0 getirilecek.
invoice_product_df = df.pivot_table(columns=["Hizmet"],
                                    index=["SepetID"],
                                    values=["ServiceId"],
                                    aggfunc="count").fillna(0).applymap(lambda x: 1 if x > 0 else 0)
# Hizmet         0_8  10_9  11_11  12_7  13_11  14_7  15_1  16_8  17_5  18_4..
# SepetID
# 0_2017-08        0     0      0     0      0     0     0     0     0     0..
# 0_2017-09        0     0      0     0      0     0     0     0     0     0..
# 0_2018-01        0     0      0     0      0     0     0     0     0     0..
# 0_2018-04        0     0      0     0      0     1     0     0     0     0..
# 10000_2017-08    0     0      0     0      0     0     0     0     0     0..


#Örneğin, 4. satır 6. sütunda NaN yerine 1 değeri bulunmaktadır. Satırda 0_2018–04 ifadesi sütunda 14_07 ifadesi bulunan matris kesişiminde yer alan 1 bizlere; 0 müşteri ID’sine sahip kullanıcının Nisan 2018'de almış olduğu 14 numaralı servis, 7 numaralı kategoriye sahip olan hizmetin satın alınmış olduğunu ifade etmektedir. 0 numaralı ID’ye sahip müşteri eğer bu tarihte başka bir hizmet alım işlemi yapmadıysa, satırın geri kalanı NaN olarak görünecektir.
df_pivot = df.pivot_table(df, index="SepetID", columns="Hizmet", aggfunc={"CategoryId": "count"}).fillna("0").astype(int)
df_pivot = df_pivot.astype(bool).astype(int)
df_pivot = df_pivot.droplevel(0, axis=1)
df_pivot

# Adım 2: Birliktelik kurallarını oluşturunuz.

frequent_itemsets = apriori(df_pivot,
                            min_support=0.01,
                            use_colnames=True)

frequent_itemsets.sort_values("support", ascending=False)

rules = association_rules(frequent_itemsets,
                          metric="support",
                          min_threshold=0.01)


rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]



rules[(rules["support"]>0.05) & (rules["confidence"]>0.1) & (rules["lift"]>5)]. \
sort_values("confidence", ascending=False)

#Adım 3: arl_recommender fonksiyonunu kullanarak en son 2_0 hizmetini alan bir kullanıcıya hizmet önerisinde bulununuz.

df.loc[df["Hizmet"] == "2_0"].sort_values("CreateDate", ascending=False)

df["CreateDate"].max() #Timestamp('2018-08-06 16:04:00')

#       UserId  ServiceId  CategoryId          CreateDate Hizmet        SepetID
#162519   10591          2           0 2018-08-06 14:43:00    2_0  10591_2018-08

rules["antecedents"] = rules["antecedents"].apply(lambda x: list(x)[0]).astype("unicode")
rules["consequents"] = rules["consequents"].apply(lambda x: list(x)[0]).astype("unicode")
rules.loc[rules["antecedents"] == "2_0"]

recommendation_list = [rules["consequents"].iloc[i] for i, antecedent in enumerate(rules["antecedents"]) if
                       antecedent == "2_0"]
recommendation_list

###['15_1', '22_0', '25_0', '13_11', '38_4']





frequent_itemsets = apriori(df_pivot, min_support=0.01, use_colnames=True)

rules = association_rules(frequent_itemsets, metric="support", min_threshold=0.01)

rules = rules.sort_values("confidence", ascending=False)

rules


