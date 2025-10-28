import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import QTimer
from UI.dado_sexy import Ui_Sexy   # importa a interface gerada pelo Qt Designer


class Jogo(QWidget, Ui_Sexy):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Conectar o botão à função de iniciar a rolagem
        self.imgbnt.clicked.connect(self.iniciar_rolagem)

        # Criar um timer para a animação
        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_dado)

        # Variáveis de controle
        self.contador = 0
        self.numero_final = 1

    def iniciar_rolagem(self):
        """Inicia a animação do dado"""
        self.contador = 0
        self.timer.start(100)  # troca a cada 100ms

    def atualizar_dado(self):
        """Troca a imagem do dado durante a animação"""
        numero = random.randint(1, 22)
        self.imgbnt.setIcon(QtGui.QIcon(f"Img/{numero}.png"))
        self.contador += 1

        # Depois de 10 trocas, para a animação e mostra o número final
        if self.contador > 10:
            self.timer.stop()
            self.numero_final = numero
            print(f"Dado final: {self.numero_final}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = Jogo()
    janela.show()
    sys.exit(app.exec_())