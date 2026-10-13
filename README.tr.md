# reaction-time-experiment

[English](README.md)

Tam ekranda hızlı ve rastgele sıralı bir görüntü dizisi gösteren, katılımcının tuş yanıtını ve tepki süresini milisaniye cinsinden kaydeden küçük bir pygame programı.

2023'te bir veri toplama çalışması için elle yazıldı.

## Ne ölçüyor

Her çalıştırma 100 denemeden oluşur. Bir denemede katılımcı SPACE'e basana kadar odak artısı gösterilir, ardından saniyede 10 görüntü hızında bir dizi oynatılır. Deneme tipine göre karıştırılmış temel diziye bir "hedef" görüntü (T2) ve çoğu tipte bir "dikkat dağıtıcı" görüntü (T1) eklenir. Dizi bitince katılımcı 2 saniye içinde `B` (evet) veya `M` (hayır) ile yanıt verir. Program yanıtın beklenenle uyuşup uyuşmadığını ve tepki süresini (ms) kaydeder.

Deneme tipleri (sonuç dosyasında `Soru Tipi` olarak yazılan sayı):

| Tip | İçerik |
|-----|--------|
| 0 | dikkat dağıtıcı, 3 kare (300 ms) sonra hedef |
| 1 | hedef gösterilmez, soru yine sorulur |
| 2 | hedef, 2 kare sonra dikkat dağıtıcı |
| 3 | yalnızca hedef |
| 4 | dikkat dağıtıcı, 5 kare (500 ms) sonra hedef |

Deneme tiplerinin ve görüntülerin sırası her çalıştırmada rastgeledir. Tip 1 dışındaki tüm tiplerde `B` (evet) doğru sayılır; tip 1'de `M` (hayır) doğru sayılır. (Katılımcıya tam olarak ne sorulduğu kodda belirtilmemiştir.)

## Gereksinimler ve kurulum

- Python 3.8+ (3.11 ile denendi)
- `pip install -r requirements.txt` (pygame)
- Pencere 1366x768 sabit boyutta ve tam ekrandır.

## Uyaranlar

Bu projeyle görsel dağıtılmaz. Kendi görsellerinizi `stimuli/` içine koyun ([stimuli/README.md](stimuli/README.md)) ya da nötr, renkli şekillerden oluşan yer tutucular üretin:

```
python src/make_placeholder_stimuli.py
```

## Çalıştırma

Depo kök klasöründen:

```
python -m src.experiment --group male
python -m src.experiment --group female
```

Seçenekler: `--stimuli KLASÖR` (varsayılan `stimuli/`), `--results DOSYA` (varsayılan `data/results_<group>.txt`).

`--group`, `stimuli/<group>/` alt klasörünü seçer. Özgün çalışma, her grup için neredeyse aynı iki programdan oluşuyordu; tek mantık farkı rastgele ekleme konumunun üst sınırıydı (10 ve 11) ve grup başına ayar olarak korunmuştur. Geri kalan her şey birleştirildi.

## Tuşlar

| Tuş | İşlev |
|-----|-------|
| SPACE | yönergeyi ilerlet / denemeyi başlat |
| B (evet) veya M (hayır) | dizi sonunda yanıt |
| ESC | çıkış (bu sürümde eklendi; tam ekran pencerenin çıkışı yoktu) |

## Sonuç dosyası

Her deneme için `data/results_<group>.txt` dosyasına (git'e alınmaz) bir satır eklenir:

```
Soru Tipi: <tip> ==> DOGRU|YANLIS ==> CEVAPLAMA SURESI (ms): <ms>
Soru Tipi: <tip> ==> YANLIS(BOS)
```

İkinci biçim 2 saniye içinde yanıt verilmediğinde yazılır ("DAHA HIZLI OLUN!" gösterilir). Tepki süresi yanıt istemi göründüğü andan ölçülür. Dosyaya ekleme yapılır, üzerine yazılmaz; katılımcı veya oturum kimliği içermez.

## Bilinen sınırlar

- Rastgelelik tohumlanmaz ve kaydedilmez; bir denemedeki gerçek görüntü sırası saklanmaz.
- Yalnızca deneme tipi, doğruluk ve süre saklanır; zaman damgası, katılımcı kimliği ve basılan tuşun kendisi yoktur.
- 101 tip girdisinden tam 100 deneme kullanılır; bu yüzden her çalıştırmada tip 1 sayısı 20 veya 21 olur.
- Görüntüler ölçeklenmez; yaklaşık 225x225 px varsayımıyla sabit konuma çizilir. Çözünürlük sabittir.
- Yanıt isteminden önce basılan tuşlar kontrol edilmez; zamanlama basit bir kare saatine dayanır ve milisaniye hassasiyetli sunum zamanlaması için kalibre edilmemiştir.
- Yönerge slaytları isteğe bağlı görsellerdir; yoksa düz Türkçe bir metin ekranı gösterilir. Ekran metinleri Türkçedir.
- Ekleme konumları yaklaşık 11 görüntülük temel diziyi varsayar; daha az görüntüde aralıklar değişebilir.
- Özgün projenin diğer bileşenleri bu depoya dahil değildir.

## Lisans

MIT, bkz. [LICENSE](LICENSE).
