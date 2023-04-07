https://www.mazegenerator.net/

Labirentleri bu websitesinden generate ettim ve maze_samples içerisine olabilecek EN ZOR labirentleri yerleştirdim.
Labirentleri pdf olarak kaydedip ekran görüntülerini alıp gerekli yerlere başlangıç ve bitiş noktasını belirten okları yerleştirdim.

*Labirentin başlangıç noktası kırmızı ok ve bitiş noktası yeşil ok ile belirtilmelidir.*

*Harici renkler kabul edilmemektedir. Threshold aralığı yüzünden tonları ayırt edilmektedir ve kırmızı ile yeşil ok farkı anlaşılır.*

*Başlangıç: Kırmızı ok ucu*

*Bitiş: Yeşil ok ucu*

*Aşağıda anlatılan Kaggle dataset test edilirken ok verilmesine gerek yoktur ilgili bitiş ve başlangıç noktası yapay zeka tarafından belirlenir.*

Çözülmesi istenen labirent main.py içerisinde maze.solve_maze() şeklinde parametre olarak dosya ismi verilir.

Labirentler 'maze_samples' dosyasının içerisine koyulmalıdır.'

Labirentlerin çözümü results dosyası içerisinde bulunmaktadır.

Ben siz test edecek kişi için zorlu labirentler oluşturdum ve maze_samples içerisine koyup ayrıca kendim test ettim.
Programın başarımını test etmek için kaggle'dan labirent dataseti indirdim ve gerekli test'i onun da üzerinde yapabilirsiniz.

KAGGLE DATASET LİNK: https://www.kaggle.com/datasets/emadehsan/rectangular-maze-kruskals-spanning-tree-algorithm

Eğer kaggle_dataset test ediyorsanız, en son kısma True parametresini vermelisiniz. Çünkü başlangıç ve bitiş noktaları belli değil

1000 tane labirent resmininin başlangıç ve bitişine ok çizmek kontrol eden kişi için neredeyse imkansız olacağı için başlangıç ve bitişi yapay zeka belirlemektedir.

sonuçlar 'kaggle_results' içerisina kaydedilir.

ÖRNEK:

maze.solve_maze(val, True)
