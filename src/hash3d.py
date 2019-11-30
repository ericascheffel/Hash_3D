from time import sleep
import copy
import serial

leitura = object()  # serial.Serial('COM7', 9600)


class Tabuleiro:
    def __init__(self):
        self.casa = [[[0, 0, 0]for _ in range(3)]for __ in range(3)]
        self.valor = ""
        self.peca_cor = self.peca_dot = self.casa
        self.atualiza()

    def atualiza(self, arduino=(0,)*27):
        arduino = [arduino[0:9], arduino[9:18], arduino[18:27]]
        self.casa = [[linha[0:3], linha[3:6], linha[6:9]] for linha in arduino]
        self.peca_cor = copy.deepcopy(self.casa)
        self.peca_dot = copy.deepcopy(self.casa)
        self.peca_cor = [[[(int(peca)-1)//5+1 for peca in linha] for linha in nivel] for nivel in self.peca_cor]
        self.peca_dot = [[[(int(peca)-1) % 5+1 if int(peca) else 0 for peca in linha]
                          for linha in nivel] for nivel in self.peca_dot]
        return self.pontua(self.peca_cor) + self.pontua(self.peca_dot)

    def pontua(self, cubo):
        pontos = self.crivo(cubo)
        # [print(nivel) for nivel in cubo]
        linhas_y = [zip(*nivel) for nivel in cubo]
        # [print([[x for x in y] for y in nivel]) for nivel in linhas_y]
        pontos += self.crivo(linhas_y)
        linhas_z = [[[casa for casa in linha] for linha in nivel] for nivel in zip(*cubo)]
        # [print([[x for x in y] for y in nivel]) for nivel in linhas_z]
        pontos += self.crivo(linhas_z)
        colunas_z = [[[casa for casa in linha] for linha in zip(*nivel)] for nivel in zip(*cubo)]
        [print([[x for x in y] for y in nivel]) for nivel in colunas_z]
        pontos += self.crivo(colunas_z)
        linhas_x = [zip(*[[casa for casa in linha] for linha in nivel]) for nivel in cubo]
        pontos += self.crivo(linhas_x)

        print("Número de acertos", pontos)
        return pontos

    @staticmethod
    def crivo(tabuleiro_):
        return sum([1 if (len(set(linha)) == 1 and 0 not in linha) else 0 for nivel in tabuleiro_ for linha in nivel])

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
            tabuleiro.atualiza(atualizador)
            # print("tabuleiro",tabuleiro.casa)
            [print(linha) for nivel in tabuleiro.casa for linha in nivel]


def main():
    tabuleiro_ = Tabuleiro()
    return tabuleiro_


if __name__ == '__main__':
    tabuleiro = main()
    velha = tabuleiro.atualiza(list(range(1, 28)))
    print("Numero de velhas", velha)

    '''verticais_ = [zip(*nivel) for nivel in tabuleiro.peca_cor]
    verticais_ = [[[casa for casa in linha] for linha in nivel]for nivel in verticais_]
    altitudes = [[[casa for casa in linha] for linha in nivel]for nivel in zip(*tabuleiro.peca_cor)]
    azimutes = [[[casa for casa in linha] for linha in zip(*nivel)]for nivel in zip(*tabuleiro.peca_cor)]

    [print(nivel) for nivel in tabuleiro.peca_cor]
    [print(nivel) for nivel in altitudes]
    [print(nivel) for nivel in azimutes]'''
    # [print(nivel) for nivel in verticais_]
    # assert tabuleiro.casa[0][0] == [1,0,0], f" mas era {tabuleiro.casa[0][0]}"
    # tabuleiro.atualiza([2]+[0]*26)
    # assert tabuleiro.casa[0][0] == [2, 0, 0], f" mas era {tabuleiro.casa[0][0]}"

    for i in range(0):
        tabuleiro.leitor()
        sleep(1)
