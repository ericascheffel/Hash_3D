import copy
from time import sleep
import serial
import logging
logging.basicConfig(level=logging.INFO)
# leitura = serial.Serial('COM7', 9600)


class Tabuleiro:
    def __init__(self, leitor, debug="no"):
        self.casa = [[[0, 0, 0]for _ in range(3)]for __ in range(3)]
        self.valor, self._leitor = "", leitor
        self.peca_cor = self.peca_dot = self.casa
        self.debug = debug
        self.atualiza()

    def atualiza(self, arduino=(0,)*27):
        arduino = [arduino[0:9], arduino[9:18], arduino[18:27]]
        self.casa = [[linha[0:3], linha[3:6], linha[6:9]] for linha in arduino]
        self.peca_cor = copy.deepcopy(self.casa)
        self.peca_dot = copy.deepcopy(self.casa)
        self.peca_cor = [[[(int(peca)-1)//5+1 for peca in linha] for linha in nivel] for nivel in self.peca_cor]
        self.peca_dot = [[[(int(peca)-1) % 5+1 + (int(peca)-1)//15 if int(peca) else 0 for peca in linha]
                          for linha in nivel] for nivel in self.peca_dot]
        return self.pontua(self.peca_cor) + self.pontua(self.peca_dot)

    def pontua(self, cubo):
        pontos = self.crivo(cubo)
        diag = ([[linha[desloca:][0]
                  for desloca, linha in enumerate(nivel)] for nivel in cubo],
                [[linha[:3 - desloca:][-1]
                  for desloca, linha in enumerate(nivel)] for nivel in cubo])
        # logging.debug(diag)
        pontos += self.crivo(diag)
        # [logging.debug(nivel) for nivel in cubo]
        linhas_z = list(zip(*[[[casa for casa in linha] for linha in zip(*nivel)] for nivel in cubo]))
        # linhas_z = [[[casa for casa in linha] for linha in nivel] for nivel in zip(*cubo)]
        # [logging.debug([[x for x in y] for y in nivel]) for nivel in linhas_z]
        diag = ([[linha[desloca:][0]
                  for desloca, linha in enumerate(nivel)] for nivel in linhas_z],
                [[linha[:3 - desloca:][-1]
                  for desloca, linha in enumerate(nivel)] for nivel in linhas_z])
        # logging.debug(diag)
        pontos += self.crivo(diag)
        pontos += self.crivo(linhas_z)
        colunas_z = [[[casa for casa in linha] for linha in zip(*nivel)] for nivel in zip(*cubo)]
        [logging.debug(f"debug:{self.debug}/{inivel}:{[[x for x in y] for y in nivel]}")
         for inivel, nivel in enumerate(colunas_z)]
        diag = ([[linha[desloca:][0]
                  for desloca, linha in enumerate(nivel)] for nivel in colunas_z],
                [[linha[:3 - desloca:][-1]
                  for desloca, linha in enumerate(nivel)] for nivel in colunas_z])
        # print(diag)
        pontos += self.crivo(diag)
        # print(self.mostra(cubo))
        logging.debug("debug:{} Cubo: {}".format(self.debug, self.mostra(cubo)))
        diagz0 = [[linha[desloca:][0] for desloca, linha in enumerate(nivel)]for nivel in colunas_z]
        diagz1 = [[linha[:3 - desloca:][-1] for desloca, linha in enumerate(nivel)]for nivel in colunas_z]
        pontos += self.crivo([diagz0, diagz1])
        pontos += self.crivo(colunas_z)
        diagx0 = [cubo[0][0][0],cubo[1][1][1],cubo[2][2][2]]
        diagx1 = [cubo[0][0][2],cubo[1][1][1],cubo[2][2][0]]
        diagy0 = [cubo[0][2][0],cubo[1][1][1],cubo[2][0][2]]
        diagy1 = [cubo[0][2][2],cubo[1][1][1],cubo[2][0][0]]
        diagonais = [[diagx0, diagx1], [diagy0, diagy1]]
        pontos += self.crivo(diagonais)
        fdiagonais = "debug:{} diagonais - x0:{} x1:{} y0:{} y1:{} z0:{} z1:{}"
        logging.debug(fdiagonais.format(self.debug, diagx0, diagx1, diagy0, diagy1, diagz0, diagz1))

        # print("Número de acertos", pontos)
        return pontos

    @staticmethod
    def mostra(tabuleiro_):
        mostra = "{}{}{} "*9
        return mostra.format(*[peca for nivel in tabuleiro_ for linha in nivel for peca in linha])

    @staticmethod
    def crivo(tabuleiro_):
        return sum([1 if (len(set(linha)) == 1 and 0 not in linha) else 0 for nivel in tabuleiro_ for linha in nivel])

    def _leitor(self):
        lido = self._leitor.readline().decode("utf8") + ":"
        lido = lido.split()
        pontos = self.atualiza(lido)

        logging.info("Número de acertos", pontos)
        return pontos

    def leitor(self):
        lido = self._leitor.readline().decode("utf8") + ":"
        lido = " ".join(lido.split())
        lido = lido.replace(":", " ")
        self.valor += lido
        tripa = self.valor.split("Nova Leitura")
        # print(f"tripa : {self.valor}, {tripa}")
        if len(tripa) > 2:
            atualizador = tripa[1].split()
            self.valor = ""
            # logging.info(atualizador)
            logging.info("Cubo: {}".format(self.mostra(atualizador)))
            pontos = self.atualiza(atualizador)
            logging.info(f"Número de acertos: {pontos}")
            self.valor = ''
            # print("tabuleiro",tabuleiro.casa)
            # [print(linha) for nivel in tabuleiro.casa for linha in nivel]
            return pontos
        return -1


class FalsoSerial:

    def readline(self):
        return b' 0 0 0 0 0 0 0 0 0\n 0 0 0 0 0 0 0 0 0\n 0 0 0 0 0 0 0 0 0\n'


def main():
    # tabuleiro_ = Tabuleiro(FalsoSerial()) #(serial.Serial('COM7', 9600))
    tabuleiro_ = Tabuleiro(serial.Serial('/dev/ttyACM0', 9600))
    return tabuleiro_


if __name__ == '__main__':
    tabuleiro = main()
    for i in range(1200):
        tabuleiro.leitor()
        sleep(0.5)
