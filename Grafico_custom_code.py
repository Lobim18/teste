from PyQt5 import uic,QtWidgets #importação das bibliotecas
import matplotlib.pyplot as plt
from  PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QVBoxLayout,QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import datetime

#criação de variaveis usadas no codigo.
xgrafico = []
ygrafico = []
tempo = -1
permicao = False
velocidade= 500
max_grafic = 8
opcao = 1

# classe usada para fazer o grafico funcionar e aparecer  em tempo real
class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        # Cria a Figure e o Axes
        self.fig, self.axes = plt.subplots(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
#classe principal do codigo
class janela(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("Grafico-custom.ui", self) #conceta a o arquivo do Qtdesigner que é o .ui
        #conecta os botãos ao os def que vao ser executados quando o botão for clicado
        self.comecar1.clicked.connect(self.continuar)
        self.para.clicked.connect(self.parar)
        self.B_atualizar.clicked.connect(self.atualizar)
        self.bot_mudar.clicked.connect(self.por_manualmente)
        self.bt_ad10.clicked.connect(self.ad10)
        self.bt_ad1.clicked.connect(self.ad1)
        self.bt_ti1.clicked.connect(self.ti1)
        self.bt_ti10.clicked.connect(self.ti10)
        self.bo_colocar.clicked.connect(self.maximo_pontos)
        self.Reinicia.clicked.connect(self.reinicar)

        self.combo_tipo.activated.connect(self.tipo_x)

        self.actionImagen_Grafico.triggered.connect(self.salvar) #conecta a ação salvar a variavel salvar.

        # salva a classe MplCanvas como uma variavel
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        #adiciona o canvas no layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.graficozin.setLayout(layout)

        self.dados_set =0 #seta o dado set = a 0

        #conecta o Qdial ao Qslide
        self.controle.valueChanged.connect(self.dial.setValue)
        self.dial.valueChanged.connect(self.controle.setValue)
        #configura o tempo que demora para arualizar po grafico
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.temporisador)
        self.timer.start(velocidade)


        self.show() # faz a janela do aplicativo aparecer no windows

    def temporisador(self): #varavel que faz o grafico atualizar a cada tatos segundos , ela faz isso rodando o def do inicio
        if permicao == True:
            self.inicio()

    def atualizar(self): # muda o tempo de atualização depedendo do que está na Qline linha
        global velocidade
        dados = int(self.linha.text())
        print(dados)
        velocidade = dados
        print(velocidade)
        self.timer.start(velocidade)

    def por_manualmente(self): # a varivael muda a quantidade do qslide para o numero especifico posto na linha Line_va
       self.dados_set = int(self.line_va.text())
       print(self.dados_set)
       self.controle.setValue(self.dados_set)

    def ad10 (self):#adiciona mais 10 no mumero da line_va
        self.dados_set = self.dados_set+10
        self.controle.setValue(self.dados_set)
        self.line_va.setText(str(self.dados_set))

    def ad1 (self): #adiciona mais 1 no mumero da line_va
        self.dados_set = self.dados_set+1
        self.controle.setValue(self.dados_set)
        self.line_va.setText(str(self.dados_set))

    def ti1(self):#subtrai 1 do mumero da line_va
        if  self.dados_set >0:
            self.dados_set = self.dados_set-1
            self.controle.setValue(self.dados_set)
            self.line_va.setText(str(self.dados_set))

    def ti10(self):#subtrai 10 do mumero da line_va
        if self.dados_set > 9:
            self.dados_set = self.dados_set - 10
            self.controle.setValue(self.dados_set)
            self.line_va.setText(str(self.dados_set))

    def maximo_pontos (self):  #ele modifica o maxiom de ontos possiveis simultaneamente no grafico
        global max_grafic
        max_grafic = int(self.line_nu.text())

    def reinicar(self):  # reinicia o grafico
        global xgrafico, ygrafico, tempo
        xgrafico.clear()
        ygrafico.clear()
        tempo = 0
        self.canvas.axes.cla()
        self.canvas.axes.set_title("Gráfico em tempo real")
        self.canvas.axes.set_ylabel("x")
        self.canvas.axes.set_ylabel("Y")
        self.canvas.draw_idle()

    def tipo_x (self):
        global opcao,xgrafico,ygrafico
        tipoo1 =self.combo_tipo.currentText()

        if tipoo1 =="quantidade pontos":
            opcao =1
            self.reinicar()

        if tipoo1 == "Tempo em segundos":
            opcao = 2
            self.reinicar()

        if tipoo1 == "Tempo em milesegundos":
            opcao = 3
            self.reinicar()



    def salvar (self): #def que faz salavr o grafico
        salvando, _ = QFileDialog.getSaveFileName(
            self,
            "Salvar imagen do gráfico como…",
            "",
            "PNG (*.png);;JPEG (*.jpg);;PDF (*.pdf)"
        )
        if salvando:
            self.canvas.figure.savefig(salvando)

    def inicio (self): # def principal do godigo que nele é proogramada a atualização do grafico
        salvar = self.controle.value() # salva na variavel salvar o valor do Qslider
        print(salvar)
        global  xgrafico ,ygrafico ,tempo, opcao
        tempo +=1
        tempo_real =datetime.datetime.now()
        if opcao == 1:
            xgrafico.append(tempo)
        if opcao == 2:
            tps =tempo_real.strftime("%H:%M:%S")
            xgrafico.append(tps),

        if opcao == 3:
            tpms =tempo_real.strftime("%M:%S:%f")
            xgrafico.append(tpms)
        ygrafico.append(salvar)
        print(xgrafico)
        print(ygrafico)

        #salva os tamahnos para verificar se ele é maior que o limite
        tamanho =len(xgrafico)
        tamanho2 = len(ygrafico)
        if tamanho >max_grafic:
            xgrafico.pop(0)

        if tamanho2 > max_grafic:
            ygrafico.pop(0)
        salvar =str(salvar)
        self.label_v.setText("Valor atual ="+salvar)# poem o valor atual numa label

        self.canvas.axes.cla() # apaga a antiga versão do grafico para não ter erros
        # cria o grafico com ou sem pontos aprecendo
        if self.pontos.isChecked():
            self.canvas.axes.plot(xgrafico, ygrafico,'-o')
        else:
            self.canvas.axes.plot(xgrafico, ygrafico)
        #poem informações do grafico
        self.canvas.axes.set_title("Gráfico em tempo real")
        self.canvas.axes.set_xlabel("x")
        self.canvas.axes.set_ylabel("Y")

        self.canvas.draw_idle()#faz o grafico aparcer




    def continuar(self): # faz o grafico voltar a atualizar
        global permicao
        permicao = True

    def parar(self): # faz o grafico parar de atualizar
        global permicao
        permicao =False


# executa o app
app=QtWidgets.QApplication([])
UiWindow =janela()
app.exec_()

