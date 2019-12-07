import copy
from time import sleep
import serial

leitura = serial.Serial('COM7', 9600)

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
        diag = ([[linha[desloca:][0]
                   for desloca, linha in enumerate(nivel)] for nivel in cubo],
                [[linha[:3 - desloca:][-1]
                   for desloca, linha in enumerate(nivel)] for nivel in cubo])
        # print(diag)
        pontos += self.crivo(diag)
        # [print(nivel) for nivel in cubo]
        linhas_z = list(zip(*[[[casa for casa in linha] for linha in zip(*nivel)] for nivel in cubo]))
        # linhas_z = [[[casa for casa in linha] for linha in nivel] for nivel in zip(*cubo)]
        # [print([[x for x in y] for y in nivel]) for nivel in linhas_z]
        diag = ([[linha[desloca:][0]
                   for desloca, linha in enumerate(nivel)] for nivel in linhas_z],
                [[linha[:3 - desloca:][-1]
                   for desloca, linha in enumerate(nivel)] for nivel in linhas_z])
        # print(diag)
        pontos += self.crivo(diag)
        pontos += self.crivo(linhas_z)
        colunas_z = [[[casa for casa in linha] for linha in zip(*nivel)] for nivel in zip(*cubo)]
        # [print([[x for x in y] for y in nivel]) for nivel in colunas_z]
        diag = ([[linha[desloca:][0]
                   for desloca, linha in enumerate(nivel)] for nivel in colunas_z],
                [[linha[:3 - desloca:][-1]
                   for desloca, linha in enumerate(nivel)] for nivel in colunas_z])
        # print(diag)
        pontos += self.crivo(diag)
        print(self.mostra(cubo))
        diagz0 = [[linha[desloca:][0] for desloca, linha in enumerate(nivel)]for nivel in colunas_z]
        diagz1 = [[linha[:3 - desloca:][-1] for desloca, linha in enumerate(nivel)]for nivel in colunas_z]
        pontos += self.crivo([diagz0, diagz1])
        pontos += self.crivo(colunas_z)
        print(diagx0, diagx1, diagy0, diagy1, diagz0, diagz1)

        # print("Número de acertos", pontos)
        return pontos

    @staticmethod
    def mostra(tabuleiro_):
        mostra = "{}{}{} "*9
        return mostra.format(*[peca for nivel in tabuleiro_ for linha in nivel for peca in linha])

    @staticmethod
    def crivo(tabuleiro_):
        return sum([1 if (len(set(linha)) == 1 and 0 not in linha) else 0 for nivel in tabuleiro_ for linha in nivel])

    def leitor(self):
        lido = leitura.readline().decode("utf8") + ":"
        lido = lido.split()
        tabuleiro.atualiza(lido)

    def _leitor(self):
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
    
    '''pontos = tabuleiro.atualiza(list(range(1, 28)))
    assert 10 == pontos, f"no entanto deu {pontos}"
    pontos = tabuleiro.atualiza([1]*27)
    assert 54 == pontos, f"no entanto deu {pontos}"
    print("Numero de pontos", pontos)

    verticais_ = [zip(*nivel) for nivel in tabuleiro.peca_cor]
    verticais_ = [[[casa for casa in linha] for linha in nivel]for nivel in verticais_]
    altitudes = [[[casa for casa in linha] for linha in nivel]for nivel in zip(*tabuleiro.peca_cor)]
    azimutes = [[[casa for casa in linha] for linha in zip(*nivel)]for nivel in zip(*tabuleiro.peca_cor)]

    [print(nivel) for nivel in tabuleiro.peca_cor]
    [print(nivel) for nivel in altitudes]    

    [print(nivel) for nivel in azimutes]
    # [print(nivel) for nivel in verticais_]
    # assert tabuleiro.casa[0][0] == [1,0,0], f" mas era {tabuleiro.casa[0][0]}"
    # tabuleiro.atualiza([2]+[0]*26)
    # assert tabuleiro.casa[0][0] == [2, 0, 0], f" mas era {tabuleiro.casa[0][0]}"
    LL = (0,1,2)
    # mx = [9*k+3*j+i+1 for k in LL for j in LL for i in LL]
    form = "{}"*3
    bform = "|"+f"{form} {form} {form}|"*3
    print(bform)
    # print(form.format(*mx))
    for n, m in [(j, i) for j in LL for i in LL]:
        mx = [1 if (k, j) == (n, m) else 0 for k in LL for j in LL for i in LL]
        cnt = tabuleiro.atualiza(mx)
        assert cnt == 2, f"but was {cnt} in {bform.format(*mx)}"
        # print(" ".join(str(x) for x in mx))
    for n, m in [(j, i) for j in LL for i in LL]:
        mx = [1 if (k, i) == (n, m) else 0 for k in LL for j in LL for i in LL]
        cnt = tabuleiro.atualiza(mx)
        assert cnt == 2, f"but was {cnt} in {bform.format(*mx)}"
        # print(" ".join(str(x) for x in mx))
    for n, m in [(j, i) for j in LL for i in LL]:
        mx = [1 if (j, i) == (n, m) else 0 for k in LL for j in LL for i in LL]
        cnt = tabuleiro.atualiza(mx)
        assert cnt == 2, f"but was {cnt} in {bform.format(*mx)}"
    print("-"*30)
    for n, m in [(j, i) for j in LL for i in LL]:
        mx = [1 if j == i and k == n else 0 for k in LL for j in LL for i in LL]
        cnt = tabuleiro.atualiza(mx)
        assert cnt == 2, f"but was {cnt} in {bform.format(*mx)}"
        # print(" ".join(str(x) for x in mx))
    for n, m in [(j, i) for j in LL for i in LL]:
        mx = [1 if j == k and i == n else 0 for k in LL for j in LL for i in LL]
        cnt = tabuleiro.atualiza(mx)
        assert cnt == 2, f"but was {cnt} in {bform.format(*mx)}"
        # print(" ".join(str(x) for x in mx))
    for n, m in [(j, i) for j in LL for i in LL]:
        mx = [1 if i == k and j == n else 0 for k in LL for j in LL for i in LL]
        cnt = tabuleiro.atualiza(mx)
        assert cnt == 2, f"but was {cnt} in {bform.format(*mx)}"
        # print(" ".join(str(x) for x in mx))'''
    
    for i in range(0):    
        tabuleiro.leitor()
        sleep(1)
