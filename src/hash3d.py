from time import sleep
import copy
import serial

leitura = serial.Serial('COM7', 9600)

class Tabuleiro:
    def __init__(self):
        self.casa = [[[0,0,0]for y in range(3)]for z in range(3)]
        self.valor = ""
        self.peca_cor = copy.deepcopy(self.casa)
        self.peca_cor = [[[(int(peca)-1)//5+1 for peca in linha] for linha in nivel] for nivel in self.peca_cor]

    def atualiza(self, arduino = [0]*27):
        arduino = [arduino[0:9], arduino[9:18], arduino[18:27]]
        self.casa = [[linha[0:3], linha[3:6], linha[6:9]] for linha in arduino]
        self.peca_cor = copy.deepcopy(self.casa)
        self.peca_cor = [[[(int(peca) - 1) // 5+1 for peca in linha] for linha in nivel] for nivel in self.peca_cor]
        velha = self.velha(self.peca_cor)
        print ("Número de acertos", velha)
        return velha

    def velha(self, tabuleiro):
        return sum([1 if (len(set(linha)) == 1 and 0 not in linha) else 0 for nivel in tabuleiro for linha in nivel])

    def leitor(self):
        lido = leitura.readline().decode("utf8") + ":"
        lido = " ".join(lido.split())
        lido = lido.replace(":", " ")
        self.valor += lido
        tripa = self.valor.split("Nova Leitura")
        if len(tripa) > 2:
            atualizador = tripa[0].split()
            self.valor = ""
            print(atualizador)
            tabul.atualiza(atualizador)
            # print("tabuleiro",tabul.casa)
            [print(linha) for nivel in tabul.casa for linha in nivel]


def main():
    tabuleiro = Tabuleiro()
    return tabuleiro


if __name__ == '__main__' :
    tabul = main()
    #velha = tabul.atualiza(list(range(1,28)))
    #print ("Numero de velhas", velha)
    #[print(nivel) for nivel in tabul.peca_cor]
    #assert tabul.casa[0][0] == [1,0,0], f" mas era {tabul.casa[0][0]}"
    #tabul.atualiza([2]+[0]*26)
    #assert tabul.casa[0][0] == [2, 0, 0], f" mas era {tabul.casa[0][0]}"

    for i in range(30):
        tabul.leitor()
        sleep(1)
