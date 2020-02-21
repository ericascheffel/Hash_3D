import unittest
from random import shuffle

from hash3d import Tabuleiro
HEAD = "Nova Leitura\n"
LINE = " {}"*9 + "\n"
INPUT = (0,)*9*3
_ZEROES = b' 0 0 0 0 0 0 0 0 0\n 0 0 0 0 0 0 0 0 0\n 0 0 0 0 0 0 0 0 0\n'
ZEROES = b' 0 0 0 0 0 0 0 0 0'


class SerialInputMocker:
    def __init__(self, inputer=INPUT):
        self.inputer = list(inputer)
        self._stream = []
        self.line = HEAD+LINE+LINE+LINE
        self.assemble()

    def assemble(self):
        self.line = HEAD+LINE+LINE+LINE
        self._stream = self.line.format(*self.inputer)*3
        self._stream = self._stream.split("\n")

    def update(self, offset, vector, offset1=-1, vector1=(), offset2=-1, vector2=()):
        for i, v in enumerate(vector):
            self.inputer[offset+i] = v
        for i, v in enumerate(vector1):
            self.inputer[offset1+i] = v
        for i, v in enumerate(vector2):
            self.inputer[offset2+i] = v
        self.assemble()

    def readline(self):
        return self._stream.pop(0).encode("utf8")


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.i = SerialInputMocker()
        self.h = Tabuleiro(self.i)
        
    def _readall(self) -> int:
        pontos = self.h.leitor()
        while pontos < 0:
            pontos = self.h.leitor()

        return pontos

    def test_input_mocker(self):
        _input = self.i.readline()
        _HEAD = HEAD.encode("utf8")[:-1]
        self.assertEqual(_input, _HEAD, f"x {_HEAD} but was {_input}")
        _input = self.i.readline()
        self.assertEqual(_input, ZEROES, f"x {ZEROES} but was {_input}")

    def test_line00_win_both(self):
        self.i.update(0,[1]*3)
        pontua = self._readall()
        self.assertEqual(pontua, 2, f"but was {pontua}")

    def test_line00_win(self):
        self.i.update(0,[1, 2, 3])
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_line00_win_low_dot(self):
        self.i.update(0,[1, 6, 11])
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_line00_win_high_dot(self):
        self.i.update(0,[16, 26, 21])
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_line00_fail_mix_dot(self):
        self.i.update(0,[11, 26, 21])
        pontua = self._readall()
        self.assertEqual(pontua, 0, f"but was {pontua}")

    def test_diagx0_win_low_dot(self):
        self.i.update(0,[16], 13, [26], 26, [21])
        self.h.debug = "dx0_w"
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagx1_win_low_dot(self):
        self.i.update(2,[16], 13, [26], 24, [21])
        self.h.debug = "dx0_w"
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagy0_win_low_dot(self):
        self.i.update(8,[16], 13, [26], 26-8, [21])
        self.h.debug = "dx0_w"
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagy1_win_low_dot(self):
        self.i.update(6,[16], 13, [26], 26-6, [21])
        self.h.debug = "dx0_w"
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagy1_win_hi_colour(self):
        self.i.update(6,[23], 13, [24], 26-6, [25])
        self.h.debug = "dx0_w"
        pontua = self._readall()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_random_posts(self):
        posts = list(range(0,27))
        pins = list(range(1,28))
        shuffle(posts)
        shuffle(pins)
        pontua = 0
        for move, pin in zip(posts, pins):
            self.i.update(move, [pin])
            self.h.debug = "dx0_w"
            pontua += self._readall()
        self.assertGreater(pontua, 1, f"but was {pontua}")


if __name__ == '__main__':
    unittest.main()
