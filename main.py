from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import time

# Tarayıcı ayarları
chrome_options = Options()
chrome_options.add_argument("--headless")  # Tarayıcıyı arka planda çalıştırır
service = Service('C:\\Users\\demir\\OneDrive\\Desktop\\ısparta_kutuphane\\chromedriver.exe')  # Buraya ChromeDriver yolunu ekle

# Tarayıcıyı başlat
driver = webdriver.Chrome(service=service, options=chrome_options)

# Zamanı ölçmeye başla
start_time = time.time()

# Web sitesini aç
url = "https://kutuphane.isparta.edu.tr/"
#url =  "https://masalist.com/kisa-hikayeler/"
driver.get(url)

# Yükleme süresi
load_time = time.time() - start_time
print(f"Sayfa {load_time:.2f} saniyede yüklendi.")

# Sayfa kaynağını al
html_content = driver.page_source

# Tarayıcıyı kapat
driver.quit()

# Stopwords listesini yükle
stop_words = set(stopwords.words("turkish"))

# Sayfa içeriğini analiz et
soup = BeautifulSoup(html_content, "html.parser")
text = soup.get_text()

# Elde edilen texti yazdır
# print("text", text)

# Fazla boşlukları temizle
text.split()
text = " ".join(text.split())

# Büyük harfkeri küçült Türkçe'ye uygun dönüşüm
text = text.translate(str.maketrans("Iİ", "ıi")).lower()

# Noktalama işaretlerini kaldır
import string 
text = text.translate(str.maketrans("", "", string.punctuation))

# Özel işaretleri ve sayıları kaldır
import re
text = re.sub(r"[^A-Za-zÇçĞğİıÖöŞşÜü\s]","", text)

# Tokenize (kelimelere ayırma)
words = word_tokenize(text)

# İngilizce stopwords kullanıyoruz. Eğer Türkçe istiyorsan ayrıca yüklemek gerekebilir.
stop_words = set(stopwords.words("turkish"))

# Stopwords çıkarma (Kök alma yok)
filtered_words = [word.lower() for word in words if word.isalpha() and word.lower() not in stop_words]

# Eşsiz kelimeleri sayma
unique_words = set(filtered_words)
print(f"Farklı kelime sayısı: {len(unique_words)}")

# Kelimeleri yazdır
print("Kullanılan kelimeler:")
print(list(set(filtered_words)))  # Benzersiz kelimeleri listele

#print(text)

import jpype
import jpype.imports
from jpype.types import JString
import os 

# JAR dosyasının yolunu belirt
ZEMBEREK_PATH = "C:\\Users\\demir\\OneDrive\\Desktop\\ısparta_kutuphane\\zemberek-full.jar"

# JVM başlat (Zaten başlatılmadıysa)
if not jpype.isJVMStarted():
    jpype.startJVM(classpath=[ZEMBEREK_PATH])

# JVM içindeki TurkishMorphology sınıfını çağır
TurkishMorphology = jpype.JClass("zemberek.morphology.TurkishMorphology")

# Morfoloji nesnesini oluştur
morphology = TurkishMorphology.createWithDefaults()

# Kökleri saklamak için boş bir liste oluştur
root_words = []

# Edat ve bağlaç türlerini temsil eden POS etiketleri
excluded_pos_tags = ["POSTP", "CONJ"]  # POSTP = Edat, CONJ = Bağlaç

# HER KELİMEYİ ANALİZ ET VE EDAT/BAĞLAÇ DIŞINDAKİLERİ AL
for word in filtered_words:
    print(f"\nKelime: {word}")
    results = morphology.analyzeSentence(JString(word))
    for result in results:
        analysis_result = result.getAnalysisResults()
        for analysis in analysis_result:
            lemma = analysis.getLemmas()[0]  # İlk kökü al
            pos = analysis.getPos().shortForm  # Kelimenin türünü al (POS tag)
            print(f"Kök: {lemma}, Tür: {pos}")

            # Edat veya bağlaç değilse kökü listeye ekle
            if pos not in excluded_pos_tags:
                root_words.append(lemma)

# Eşsiz kökleri al ve yazdır
unique_roots = list(set(root_words))
print("\nKullanılan kelimelerin kökleri:")
print(unique_roots)
