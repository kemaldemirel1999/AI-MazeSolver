import cv2
import heapq
import os
import numpy as np
from preprocess import Preprocess


class JpgMaze:
    '''
        *JPG, JPEG ve PNG labirentlerin gidiş yolunu bulan sınıftır.
        *Başlangıç noktası: Kırmızı ok ucu
        *Bitiş noktası: Yeşil ok ucu

        *Eğer kaggle dataset test ediyorsanız başlangıç ve bitiş noktası yapay zeka tarafından bulunur.

        Bu işlemlerin nasıl yapıldığınız özeti:
        1- ilgili labirent resmi dosyadan openCV ile okunur
        2- resim içerisinde kırmızı ve yeşil ok aranır
        3- Bu okların her uç koordinat noktaları ve yönleri belirlenir.
        4- Kırmızı ok ucu start_x, start_y noktasını belirler
        5- Yeşil ok ucu end_x, end_y noktasını belirler.
        6- Bu oklar resim üzerinden kaldırılır.
        7- Bu son resim görüntü işleme teknikleri uygulayarak uygun hale getirilir ve Threshold uygulanır.
        8- Siyah noktalar: 0 ve beyaz noktalar:255 değerine sahip olmuş olur
        9- bu labirent resminde sağ, sol, üst ve aşağı kısımda boşluklar olabileceği için algoritma bu yerlerden gitmek
            isteyebilir. Bu durumda okun yönü ve yeri baz alınarak resim üzerinde kırpma işlemi uygulanır.
        10- Kırpma işlemi esnasında okların ucu (başlangıç ve bitiş noktaları) labirentin dışarısında ise ilgili labirent kapısı olacak
            başlangıç ve bitiş noktaları güncellenir.
        11- Artık elimizde başlangıç ve bitiş noktaları belirli, algoritmaya hazır olacak şekilde düzenlenmiş bir resim bulunmaktadır.
        12- A-star algoritması çalıştırılır ve başlangıç noktasından bitiş noktasına kadar olan en kısa path bulunur.
        13- -A-star algoritması çalıştırılır ve başlangıç noktasından bitiş noktasına kadar olan en kısa path bulunur.
            -Bu algoritma için heuristic fonksiyonu kullanılır.
            -Heuristic fonksiyonu hedefe kalan mesafeyi tahmin etmek için kullanılır ve bu tahmini hedef noktaya ulaşmak için
                gereken yol mesafeyiyle birleştirerek hangi yollardan gidilmesi gerektiğine karar verir.
                Bulunan her hücre için a-star algoritması başlangıç noktasından ilgili hücreye ulaşma maliyeti ile beraber
                o hücreden hedef noktaya ulaşmanın tahmini maliyetini hesaplamaktadır. a-star algoritması gerçek maliyet ile
                heuristic tahmininin toplamı en düşük olan hücreyi seçer ve komşu hücreleri queue'ya kaydeder. Algoritma hedef noktaya
                ulaşılana veya bu 'queue' boş hale gelene kadar bu işlem sürdürülür.
        14- Bulunan en kısa path kırmızı olacak şekilde boyanır ve .jpg formatında orijinal ismiyle beraber 'results' dosyasına kaydedilir.
        15- Bütün bunlardan sonra en kısa yol belirlenir, path kırmızı şekilde işaretlenir.
        16- Bu trace edilmiş resim kendi dosya ismiyle ve .jpg uzantısıyla beraber 'results' dosyasına kaydedilir.
    '''

    def __init__(self):
        self.maze_path = os.getcwd() + "/maze_samples/"  # Labirentlerin bulunduğu path
        # self.trials_path = os.getcwd() + "/trials/"
        self.kaggle_path = os.getcwd() + "/kaggle_maze_dataset/rectangular_mazes_10x10/"  # kaggle dataseti pathi
        self.results_path = os.getcwd() + "/results/"  # labirent sonuçlarını içeren path
        self.kaggle_results_path = os.getcwd() + "kaggle_results/"  # kaggle verisetinin sonuçlarını içeren path

    # Maze solver başlatılır.
    def start_maze_solver(self, filename, kaggle_dataset=False):
        self.parse_image(filename, kaggle_dataset)

    def parse_image(self, filename, kaggle_dataset):
        # Labirent openCV ile okunur ve maze değişkenine array olarak kaydedilir
        maze = self.get_maze(filename, kaggle_dataset)
        # kırmızı ve yeşil ok içerip içermediği bulunur
        if self.includes_arrow(maze, "red") and self.includes_arrow(maze, "green"):
            # Kırmızı okun yönü, koordinat bilgileri ve okun en uç koordinatları hakkında bilgi edinilir.
            maze, start_x, start_y, direction_start, left, right, up, down = self.find_arrow_coordinates(maze, "red")
            # Kırmızı okun bulunduğu bölge tamamen beyaz olacak şekilde silinir.
            maze = self.remove_arrow_from_image(maze, left, right, up, down)

            # Yeşil okun yönü, koordinat bilgileri ve okun en uç koordinatları hakkında bilgi edinilir.
            maze, end_x, end_y, direction_end, left, right, up, down = self.find_arrow_coordinates(maze, "green")
            # Yeşil okun bulunduğu bölge tamamen beyaz olacak şekilde silinir.
            maze = self.remove_arrow_from_image(maze, left, right, up, down)

            # Resim üzerinde görüntü işleme uygulanır ve işleme uygun hale getirilir.
            # Siyah noktalar:0 ve beyaz noktalar:255 olacak şekilde threshold uygulanır.
            # labirent duvarları ve boş noktalar kolay olması için kullanılır.
            maze = Preprocess().preprocess_image(maze)

            # başlangıç ve bitiş noktası arasında en kısa yol bulunurken resim tamamen labirentten oluşmayacağı için
            # bu boş noktalar labirent çözümünü etkilemeyecek şekilde kırpılır ve algoritmanın oraları boş yol olarak görmesi engellenir.
            # başlangıç ve bitiş noktaları güncellenir. Yeni labirent return edilir.
            maze, start_x, start_y, end_x, end_y = self.crop_maze(maze, start_x, start_y, end_x, end_y, direction_start,
                                                                  direction_end)
            start = (start_x, start_y)
            end = (end_x, end_y)
        else:
            # Resim üzerinde görüntü işleme uygulanır ve işleme uygun hale getirilir.
            # Siyah noktalar:0 ve beyaz noktalar:255 olacak şekilde threshold uygulanır.
            # labirent duvarları ve boş noktalar kolay olması için kullanılır.
            maze = Preprocess().preprocess_image(maze)
            # Bu labirent içerisinde ok bulunmadığı için başlangıç ve bitiş noktasını belirleriz.
            # Bitiş ve başlangıç noktasının sol veya sağ bölgedeki boş çıkışlar olarak belirlenir.
            # Hangisinin başlangıç ve bitiş noktaları olduğunun bir önemi yoktur ve algoritmayı etkilemez.
            start_x, start_y, end_x, end_y = self.find_start_end_points(maze)
            start = (start_x, start_y)
            end = (end_x, end_y)

        # bütün bu işlemlerden sonra a-star algoritması çalıştırılır.
        '''
            -A-star algoritması çalıştırılır ve başlangıç noktasından bitiş noktasına kadar olan en kısa path bulunur.
            -Bu algoritma için heuristic fonksiyonu kullanılır.
            -Heuristic fonksiyonu hedefe kalan mesafeyi tahmin etmek için kullanılır ve bu tahmini hedef noktaya ulaşmak için
                gereken yol mesafeyiyle birleştirerek hangi yollardan gidilmesi gerektiğine karar verir.
                Bulunan her hücre için a-star algoritması başlangıç noktasından ilgili hücreye ulaşma maliyeti ile beraber
                o hücreden hedef noktaya ulaşmanın tahmini maliyetini hesaplamaktadır. a-star algoritması gerçek maliyet ile 
                heuristic tahmininin toplamı en düşük olan hücreyi seçer ve komşu hücreleri queue'ya kaydeder. Algoritma hedef noktaya
                ulaşılana veya bu 'queue' boş hale gelene kadar bu işlem sürdürülür.
        '''
        traced_maze = self.a_star_algorithm(start, end, maze)

        # kaggle dataset olup olmadığına göre ilgili path içerisine resim kaydedilir.
        if not kaggle_dataset:
            cv2.imwrite(self.results_path + filename, traced_maze)
        else:
            cv2.imwrite(self.kaggle_results_path + filename, traced_maze)

    # başlangıç ve bitiş noktaları belirtilmediği (kaggle dataset için) takdirde kullanılır.
    def find_start_end_points(self, maze):
        up, down, left, right = self.get_least_coordinates(maze)
        first_col = maze[:, 0]
        last_col = maze[:, len(maze[0]) - 1]
        first_row = maze[0]
        last_row = maze[len(maze) - 1]
        start_x = -1
        start_y = -1
        end_x = -1
        end_y = -1

        start_found = False
        end_found = False
        for i in range(len(first_row)):
            if first_row[i] == 255 and not start_found:
                start_x = i
                start_y = 0
                start_found = True
                break
        for i in range(len(last_row)):
            if last_row[i] == 255 and not start_found:
                end_y = len(maze) - 1
                end_x = i
                start_found = True
                break
            elif last_row[i] == 255 and not end_found:
                end_y = len(maze) - 1
                end_x = i
                end_found = True
                break
        for i in range(len(first_col)):
            if first_col[i] == 255 and not start_found:
                start_y = i
                start_x = 0
                start_found = True
                break
            elif first_col[i] == 255 and not end_found:
                end_y = i
                end_x = 0
                end_found = True
                break
        for i in range(len(last_col)):
            if last_col[i] == 255 and not start_found:
                start_y = i
                start_x = len(maze[0]) - 1
                start_found = True
                break
            elif last_col[i] == 255 and not end_found:
                end_y = i
                end_x = len(maze[0]) - 1
                end_found = True
                break
        if not start_found or not end_found:
            return None
        else:
            return start_x, start_y, end_x, end_y

    # resmin ilgili renkte ok içerip içermediğini bulur.
    def includes_arrow(self, maze, arrow_color):
        hsv = cv2.cvtColor(maze, cv2.COLOR_BGR2HSV)
        if arrow_color == "red":
            lower_range = np.array([0, 100, 100])
            upper_range = np.array([10, 255, 255])
        elif arrow_color == "green":
            lower_range = np.array([40, 50, 50])
            upper_range = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = None
        largest_contour_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_contour_area:
                largest_contour = contour
                largest_contour_area = area
        if largest_contour is not None:
            return True
        else:
            return False

    # labirent resmini algoritmaya uygun olacak şekilde kırpma işlemi gerçekleştirilir.
    def crop_maze(self, maze, start_x, start_y, end_x, end_y, direction_start, direction_end):
        up, down, left, right = self.get_least_coordinates(maze)

        if (direction_start == "left" and direction_end == "right") \
                or (direction_end == "left" and direction_start == "right") \
                or (direction_end == "left" and direction_start == "left") \
                or (direction_end == "right" and direction_start == "right"):
            maze = maze[up:len(maze)]
            start_y = start_y - up
            end_y = end_y - up
            up, down, left, right = self.get_least_coordinates(maze)
            maze = maze[0:down + 1]
        elif (direction_start == "up" and direction_end == "down") \
                or (direction_end == "up" and direction_start == "down") \
                or (direction_end == "up" and direction_start == "up") \
                or (direction_end == "down" and direction_start == "down"):
            maze = maze[:, left:len(maze[0]) + 1]
            start_x = start_x - left
            end_x = end_x - left
            up, down, left, right = self.get_least_coordinates(maze)
            maze = maze[:, 0:right + 1]
        else:
            is_start_inside = self.is_it_inside_of_maze(maze, start_x, start_y)
            is_end_inside = self.is_it_inside_of_maze(maze, end_x, end_y)
            if is_start_inside and is_end_inside:
                maze = maze[:, left:right + 1]
                start_x = start_x - left
                end_x = end_x - left
                maze = maze[up:down + 1]
                start_y = start_y - up
                end_y = end_y - up
            elif is_start_inside:
                maze = maze[:, left:right + 1]
                start_x = start_x - left
                end_x = end_x - left
            elif is_end_inside:
                maze = maze[up:down + 1]
                start_y = start_y - up
                end_y = end_y - up
            else:
                if direction_start == "left" and direction_end == "up":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y,
                                                                           direction_start, direction_end, False)
                elif direction_start == "left" and direction_end == "down":
                    None
                elif direction_start == "right" and direction_end == "up":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y,
                                                                           direction_start, direction_end, False)
                elif direction_start == "right" and direction_end == "down":
                    None
                elif direction_start == "up" and direction_end == "left":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y,
                                                                           direction_start, direction_end, True)
                elif direction_start == "up" and direction_end == "right":
                    maze, start_x, start_y, end_x, end_y = self.crop_south(maze, start_x, start_y, end_x, end_y,
                                                                           direction_start, direction_end, True)
                elif direction_start == "down" and direction_end == "left":
                    None
                elif direction_start == "down" and direction_end == "right":
                    None

        return maze, start_x, start_y, end_x, end_y

    def crop_south(self, maze, start_x, start_y, end_x, end_y, direction_start, direction_end, isItStart):
        up, down, left, right = self.get_least_coordinates(maze)
        if direction_start == "up" and isItStart:
            maze = maze[0:down + 1]
            diff_y = len(maze) - down
            end_y = end_y - diff_y
            up, down, left, right = self.get_least_coordinates(maze)
            start_y = down - 1
        elif direction_end == "up" and not isItStart:
            maze = maze[0:down + 1]
            diff_y = len(maze) - down
            start_y = start_y - diff_y
            up, down, left, right = self.get_least_coordinates(maze)
            end_y = down - 1
        else:
            print("Wrong Crop South Input")
        return maze, start_x, start_y, end_x, end_y

    # ilgili koordinatın labirent sınırları içerisinde olup olmadığı bulunur.
    def is_it_inside_of_maze(self, maze, x_coord, y_coord):
        up = len(maze)
        left = len(maze[0])
        down = 0
        right = 0
        maze_row = maze[y_coord]
        maze_col = maze[:, x_coord]
        for col in range(len(maze_row)):
            if maze_row[col] == 0:
                if col < left:
                    left = col
                if col > right:
                    right = col
        for row in range(len(maze_col)):
            if maze_col[row] == 0:
                if row < up:
                    up = row
                if row > down:
                    down = row
        if left < x_coord < right and down > y_coord > up:
            return True
        else:
            return False

    # labirentin duvarlarının sınırlarını belirlemede kullanılır.
    def get_least_coordinates(self, maze):
        up = len(maze)
        left = len(maze[0])
        down = 0
        right = 0
        for row in range(len(maze)):
            for col in range(len(maze[0])):
                if maze[row][col] == 0:
                    if row < up:
                        up = row
                    if row > down:
                        down = row
                    if col < left:
                        left = col
                    if col > right:
                        right = col
        return up, down, left, right

    '''
            -A-star algoritması çalıştırılır ve başlangıç noktasından bitiş noktasına kadar olan en kısa path bulunur.
            -Bu algoritma için heuristic fonksiyonu kullanılır.
            -Heuristic fonksiyonu hedefe kalan mesafeyi tahmin etmek için kullanılır ve bu tahmini hedef noktaya ulaşmak için
                gereken yol mesafeyiyle birleştirerek hangi yollardan gidilmesi gerektiğine karar verir.
            Bulunan her hücre için a-star algoritması başlangıç noktasından ilgili hücreye ulaşma maliyeti ile beraber
            o hücreden hedef noktaya ulaşmanın tahmini maliyetini hesaplamaktadır. a-star algoritması gerçek maliyet ile 
            heuristic tahmininin toplamı en düşük olan hücreyi seçer ve komşu hücreleri queue'ya kaydeder. Algoritma hedef noktaya
            ulaşılana veya bu 'queue' boş hale gelene kadar bu işlem sürdürülür.
    '''
    def a_star_algorithm(self, start, end, maze_gray):
        visited = set()
        queue = [(self.heuristic(start, end), 0, start, [])]
        while queue:
            _, cost, cell, path = heapq.heappop(queue)
            if cell in visited:
                continue
            visited.add(cell)
            path = path + [cell]
            if cell == end:
                break
            for neighbor in self.neighbors(cell, maze_gray):
                if neighbor not in visited:
                    neighbor_cost = cost + 1
                    neighbor_priority = neighbor_cost + self.heuristic(neighbor, end)
                    heapq.heappush(queue, (neighbor_priority, neighbor_cost, neighbor, path))

        rgb_img = cv2.cvtColor(maze_gray, cv2.COLOR_GRAY2RGB)
        cv2.polylines(rgb_img, [np.array(path)], False, (0, 0, 255), thickness=5)
        return rgb_img

    # heuristic fonksiyonu hedef noktaya tahmini mesafeyi hesaplar
    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # komşu noktalara ulaşılır
    def neighbors(self, cell, maze):
        x, y = cell
        candidates = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        return [(nx, ny) for nx, ny in candidates if
                0 <= nx < maze.shape[1] and 0 <= ny < maze.shape[0] and maze[ny, nx] == 255]

    # labirent resmini dosyadan okur ve kaydeder.
    def get_maze(self, filename, kaggle_dataset):
        if kaggle_dataset:
            maze = cv2.imread(self.kaggle_path + filename)
        else:
            maze = cv2.imread(self.maze_path + filename)
        return maze

    # okun bütün uç noktaları belirlenir.
    def get_least_val_in_largest_contour(self, maze, largest_contour):
        up = len(maze)
        left = len(maze[0])
        down = 0
        right = 0
        for val in largest_contour:
            col = val[0][0]
            row = val[0][1]
            if row < up:
                up = row
            if row > down:
                down = row
            if col < left:
                left = col
            if col > right:
                right = col
        return up, left, down, right

    # okun resmin içerisinde bulunduğu koordinat belirlenir.
    def find_arrow_coordinates(self, maze, arrow_color):
        hsv = cv2.cvtColor(maze, cv2.COLOR_BGR2HSV)
        if arrow_color == "red":
            lower_range = np.array([0, 100, 100])
            upper_range = np.array([10, 255, 255])
        elif arrow_color == "green":
            lower_range = np.array([40, 50, 50])
            upper_range = np.array([80, 255, 255])
        mask = cv2.inRange(hsv, lower_range, upper_range)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = None
        largest_contour_area = 0
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > largest_contour_area:
                largest_contour = contour
                largest_contour_area = area
        M = cv2.moments(largest_contour)

        center_x = int(M['m10'] / M['m00'])
        center_y = int(M['m01'] / M['m00'])
        [vx, vy, x, y] = cv2.fitLine(largest_contour, cv2.DIST_L2, 0, 0.01, 0.01)
        angle = np.arctan2(vy, vx) * 180 / np.pi
        if -45 <= angle < 45:
            direction = 'right' if center_x < maze.shape[1] // 2 else 'left'
        elif 45 <= angle < 135:
            direction = 'down' if center_y < maze.shape[0] // 2 else 'up'
        elif -135 <= angle < -45:
            direction = 'up' if center_y > maze.shape[0] // 2 else 'down'
        else:
            direction = 'left' if center_x < maze.shape[1] // 2 else 'right'
        up, left, down, right = self.get_least_val_in_largest_contour(maze, largest_contour)
        x_axis = 0
        y_axis = 0
        if direction == "left":
            x_axis = left
            y_axis = center_y
        elif direction == "right":
            x_axis = right
            y_axis = center_y
        elif direction == "down":
            x_axis = center_x
            y_axis = down
        else:
            x_axis = center_x
            y_axis = up
        # coordinates = (x_axis, y_axis)
        return maze, x_axis, y_axis, direction, left, right, up, down

    # ok resim üzerinden silinir. Bu işlem için bütün uç noktalar bulunur ve dikdörtgen alan belirlenir ve değeri 255(beyaz)
    # olacak şekilde bir işlem yapılır. Ok resmi silinmiş olur.
    def remove_arrow_from_image(self, image, left, right, up, down):
        mask = np.zeros(image.shape[:2], dtype=np.uint8)
        cv2.rectangle(mask, (left, up), (right, down), 255, -1)
        result = image.copy()
        result[np.where(mask == 255)] = [255, 255, 255]
        return result
