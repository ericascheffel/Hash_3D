import unittest
from hash3d import Tabuleiro
LINE = " {}"*9 + "\n"
INPUT = (0,)*9*3
ZEROES = b' 0 0 0 0 0 0 0 0 0\n 0 0 0 0 0 0 0 0 0\n 0 0 0 0 0 0 0 0 0\n'


class SerialInputMocker:
    def __init__(self, inputer=INPUT):
        self.inputer = list(inputer)
        self.line = LINE+LINE+LINE

    def update(self, offset, vector, offset1=-1, vector1=(), offset2=-1, vector2=()):
        for i, v in enumerate(vector):
            self.inputer[offset+i] = v
        for i, v in enumerate(vector1):
            self.inputer[offset1+i] = v
        for i, v in enumerate(vector2):
            self.inputer[offset2+i] = v

    def readline(self):
        return self.line.format(*self.inputer).encode("utf8")


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.i = SerialInputMocker()
        self.h = Tabuleiro(self.i)

    def test_input_mocker(self):
        _input = self.i.readline()
        self.assertEqual(_input, ZEROES, f"but was {_input}")

    def test_line00_win_both(self):
        self.i.update(0,[1]*3)
        pontua = self.h.leitor()
        self.assertEqual(pontua, 2, f"but was {pontua}")

    def test_line00_win(self):
        self.i.update(0,[1, 2, 3])
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_line00_win_low_dot(self):
        self.i.update(0,[1, 6, 11])
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_line00_win_high_dot(self):
        self.i.update(0,[16, 26, 21])
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_line00_fail_mix_dot(self):
        self.i.update(0,[11, 26, 21])
        pontua = self.h.leitor()
        self.assertEqual(pontua, 0, f"but was {pontua}")

    def test_diagx0_win_low_dot(self):
        self.i.update(0,[16], 13, [26], 26, [21])
        self.h.debug = "dx0_w"
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagx1_win_low_dot(self):
        self.i.update(2,[16], 13, [26], 24, [21])
        self.h.debug = "dx0_w"
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagy0_win_low_dot(self):
        self.i.update(8,[16], 13, [26], 26-8, [21])
        self.h.debug = "dx0_w"
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagy1_win_low_dot(self):
        self.i.update(6,[16], 13, [26], 26-6, [21])
        self.h.debug = "dx0_w"
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")

    def test_diagy1_win_hi_colour(self):
        self.i.update(6,[23], 13, [24], 26-6, [25])
        self.h.debug = "dx0_w"
        pontua = self.h.leitor()
        self.assertEqual(pontua, 1, f"but was {pontua}")


if __name__ == '__main__':
    unittest.main()
