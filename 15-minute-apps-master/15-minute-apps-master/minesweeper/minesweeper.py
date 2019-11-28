from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import random
import time

IMG_BOMB = QImage("./images/bug.png")#导入图片
IMG_FLAG = QImage("./images/flag.png")
IMG_START = QImage("./images/rocket.png")
IMG_CLOCK = QImage("./images/clock-select.png")

NUM_COLORS = {
    1: QColor('#f44336'),
    2: QColor('#9C27B0'),
    3: QColor('#3F51B5'),
    4: QColor('#03A9F4'),
    5: QColor('#00BCD4'),
    6: QColor('#4CAF50'),
    7: QColor('#E91E63'),
    8: QColor('#FF9800')
}

LEVELS = [
    (8, 10),
    (16, 40),#难度
    (24, 99)
]

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3

STATUS_ICONS = {
    STATUS_READY: "./images/plus.png",
    STATUS_PLAYING: "./images/smiley.png",
    STATUS_FAILED: "./images/cross.png",
    STATUS_SUCCESS: "./images/smiley-lol.png",
}


class Pos(QWidget):#Qwidget的子类
    #Qwidget 是父类，具体的不同的widget是子类
    expandable = pyqtSignal(int, int)
    #define new signal pyqtSignal(types[, name[, revision=0[, arguments=[]]]])
    clicked = pyqtSignal()
    ohno = pyqtSignal()

    def __init__(self, x, y, *args, **kwargs):
        super(Pos, self).__init__(*args, **kwargs)

        self.setFixedSize(QSize(20, 20))#widget 大小

        self.x = x
        self.y = y

    def reset(self):
        self.is_start = False
        self.is_mine = False
        self.adjacent_n = 0

        self.is_revealed = False
        self.is_flagged = False

        self.update()

    def paintEvent(self, event):
        p = QPainter(self)
        #QPainter provides highly optimized functions to do most of the drawing GUI programs require.
        p.setRenderHint(QPainter.Antialiasing)
        #Use the setRenderHint() function to set or clear the currently set RenderHints .
        #constant QPainter.Antialiasing Indicates that the engine should antialias edges of primitives if possible

        r = event.rect() #rect():返回包含需要重绘区域坐标和尺寸的QRect类的对象；
        #The QRect class provides a collection of functions that return the various rectangle coordinates, and enable manipulation of these. QRect also provides functions 
        #to move the rectangle relative to the various coordinates.

        if self.is_revealed:#reveal 之后内外颜色变得和背景一样，设置颜色
            color = self.palette().color(QPalette.Background)
            outer, inner = color, color
        else:
            outer, inner = Qt.gray, Qt.lightGray

        p.fillRect(r, QBrush(inner))
        #PySide2.QtGui.QPainter.fillPath(path, brush) Fills the given path using the given brush . The outline is not drawn.
        pen = QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)
#画边框填颜色
        if self.is_revealed:
            if self.is_start:#开始
                p.drawPixmap(r, QPixmap(IMG_START))

            elif self.is_mine:#雷
                p.drawPixmap(r, QPixmap(IMG_BOMB))

            elif self.adjacent_n > 0:#普通块
                pen = QPen(NUM_COLORS[self.adjacent_n])
                p.setPen(pen)
                f = p.font()
                f.setBold(True)
                p.setFont(f)
                p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))#Qt.AlignHCenter Centers horizontally in the available space.

        elif self.is_flagged:
            p.drawPixmap(r, QPixmap(IMG_FLAG)) #drawPixmap表示画上东西 drawPixmap(r, pm)

    def flag(self):
        self.is_flagged = True
        self.update()

        self.clicked.emit()

    def reveal(self):
        self.is_revealed = True
        self.update()

    def click(self):
        if not self.is_revealed:
            self.reveal()
            if self.adjacent_n == 0:
                self.expandable.emit(self.x, self.y)

        self.clicked.emit()

    def mouseReleaseEvent(self, e):

        if (e.button() == Qt.RightButton and not self.is_revealed):
            self.flag()

        elif (e.button() == Qt.LeftButton):
            self.click()

            if self.is_mine:
                self.ohno.emit()


class MainWindow(QMainWindow):#窗口显示
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.b_size, self.n_mines = LEVELS[0] #n_mines代表等级

        w = QWidget()
        hb = QHBoxLayout()
        #The QHBoxLayout class lines up widgets horizontally

        self.mines = QLabel()
        self.mines.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

        self.clock = QLabel() # The label is created with the text 
        self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#QLabel is used for displaying text or an image. No user interaction functionality is provided.
#The visual appearance of the label can be configured in various ways, and it can be used for specifying a focus mnemonic key for another widget.
        f = self.mines.font()
        f.setPointSize(24)
        f.setWeight(75)
        self.mines.setFont(f)
        self.clock.setFont(f)

        self._timer = QTimer()
        self._timer.timeout.connect(self.update_timer)#信号调用update_timer
        self._timer.start(1000)  # 1 second timer

        self.mines.setText("%03d" % self.n_mines)
        self.clock.setText("000")

        self.button = QPushButton()#一个按钮，应该是笑脸按钮
        self.button.setFixedSize(QSize(32, 32))
        self.button.setIconSize(QSize(32, 32))
        self.button.setIcon(QIcon("./images/smiley.png"))
        self.button.setFlat(True)

        self.button.pressed.connect(self.button_pressed)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_BOMB))
        l.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        hb.addWidget(l)

        hb.addWidget(self.mines)
        hb.addWidget(self.button)
        hb.addWidget(self.clock)

        l = QLabel()
        l.setPixmap(QPixmap.fromImage(IMG_CLOCK))
        l.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        hb.addWidget(l)

        vb = QVBoxLayout()
        vb.addLayout(hb)

        self.grid = QGridLayout()
        self.grid.setSpacing(5)
#QGridLayout takes the space made available to it (by its parent layout or by the parentWidget() ), divides it up into rows and columns, and puts each widget it manages into the correct cell.
        vb.addLayout(self.grid)
        w.setLayout(vb)
        self.setCentralWidget(w)

        self.init_map()
        self.update_status(STATUS_READY)

        self.reset_map()
        self.update_status(STATUS_READY)

        self.show()

    def init_map(self):
        # Add positions to the map
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = Pos(x, y)# w 应该是对应小格子
                self.grid.addWidget(w, y, x)
                # Connect signal to handle expansion.
                w.clicked.connect(self.trigger_start)
                w.expandable.connect(self.expand_reveal)
                w.ohno.connect(self.game_over)

    def reset_map(self):
        # Clear all mine positions
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                w.reset()

        # Add mines to the positions
        positions = []
        while len(positions) < self.n_mines:
            x, y = random.randint(0, self.b_size - 1), random.randint(0, self.b_size - 1)
            if (x, y) not in positions:
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_mine = True
                positions.append((x, y))

        def get_adjacency_n(x, y):
            positions = self.get_surrounding(x, y)#周围的，positions是一个list
            n_mines = sum(1 if w.is_mine else 0 for w in positions)

            return n_mines

        # Add adjacencies to the positions
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()#self.grid = QGridLayout()
                #itemAtPosition() Returns the layout item that occupies cell (row , column ), or None if the cell is empty.
                #Returns the associated widget.
                w.adjacent_n = get_adjacency_n(x, y)

        # Place starting marker
        while True:
            x, y = random.randint(0, self.b_size - 1), random.randint(0, self.b_size - 1)
            w = self.grid.itemAtPosition(y, x).widget()
            # We don't want to start on a mine.
            if (x, y) not in positions:#初始化时 positions 是一个 mine list
                w = self.grid.itemAtPosition(y, x).widget()
                w.is_start = True

                # Reveal all positions around this, if they are not mines either.
                for w in self.get_surrounding(x, y):#将周围所有非mine的都点开
                    if not w.is_mine:
                        w.click()
                break

    def get_surrounding(self, x, y):#定义周围
        positions = []

        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                positions.append(self.grid.itemAtPosition(yi, xi).widget())

        return positions

    def button_pressed(self):
        if self.status == STATUS_PLAYING:
            self.update_status(STATUS_FAILED)
            self.reveal_map()

        elif self.status == STATUS_FAILED:
            self.update_status(STATUS_READY)
            self.reset_map()

    def reveal_map(self):    #全部reveal
        for x in range(0, self.b_size):
            for y in range(0, self.b_size):
                w = self.grid.itemAtPosition(y, x).widget()
                #itemAtPosition() Returns the layout item that occupies cell (row , column ), or None if the cell is empty.
                #Returns the associated widget.
                w.reveal()

    def expand_reveal(self, x, y):
        for xi in range(max(0, x - 1), min(x + 2, self.b_size)):
            for yi in range(max(0, y - 1), min(y + 2, self.b_size)):
                w = self.grid.itemAtPosition(yi, xi).widget()
                if not w.is_mine:
                    w.click()

    def trigger_start(self, *args):
        if self.status != STATUS_PLAYING:
            # First click.
            self.update_status(STATUS_PLAYING)
            # Start timer.
            self._timer_start_nsecs = int(time.time())

    def update_status(self, status):
        self.status = status
        self.button.setIcon(QIcon(STATUS_ICONS[self.status]))

    def update_timer(self):#根据时间决定计时器运行
        if self.status == STATUS_PLAYING:
            n_secs = int(time.time()) - self._timer_start_nsecs
            self.clock.setText("%03d" % n_secs)

    def game_over(self): #游戏结束时动作
        self.reveal_map()
        self.update_status(STATUS_FAILED)


if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    app.exec_()
    #Enters the main event loop and waits until exit() is called. Returns the value that was passed to exit() (which is 0 if exit() is called via quit() ).
