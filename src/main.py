import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMovie

class FullScreenGifApp(QMainWindow):
    def __init__(self, gif_path):
        super().__init__()
        
        # Настройка окна
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | 
            Qt.FramelessWindowHint | 
            Qt.X11BypassWindowManagerHint
        )
        
        # Центральный виджет
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        
        # Загрузка GIF
        self.movie = QMovie(gif_path)
        if not self.movie.isValid():
            QMessageBox.critical(None, "Ошибка", "Неверный GIF-файл")
            sys.exit(1)
            
        self.label.setMovie(self.movie)
        self.movie.start()
        
        # Таймер для адаптации размера
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.resize_gif)
        self.timer.start(100)
        
        # Переменная для отслеживания комбинации
        self.key_sequence = []
        self.target_sequence = [
            Qt.Key_Control,
            Qt.Key_Alt,
            Qt.Key_Shift,
            Qt.Key_Q
        ]
        
        self.showFullScreen()
    
    def resize_gif(self):
        screen_size = self.screen().size()
        self.movie.setScaledSize(screen_size)
    
    def keyPressEvent(self, event):
        # Простая и надежная проверка комбинации
        if event.key() == Qt.Key_Q:
            modifiers = QApplication.keyboardModifiers()
            if (modifiers & Qt.ControlModifier and 
                modifiers & Qt.AltModifier and 
                modifiers & Qt.ShiftModifier):
                self.close_app()
        event.ignore()
    
    def close_app(self):
        self.movie.stop()
        QApplication.quit()
    
    def closeEvent(self, event):
        event.ignore()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Укажите абсолютный путь к GIF
    gif_path = "C:\Games\mewingcat\mewing-cat.gif"  # Замените на реальный путь
    
    # Проверка файла
    try:
        with open(gif_path, 'rb'):
            pass
    except IOError:
        QMessageBox.critical(None, "Ошибка", "Файл не найден")
        sys.exit(1)
    
    window = FullScreenGifApp(gif_path)
    sys.exit(app.exec_())