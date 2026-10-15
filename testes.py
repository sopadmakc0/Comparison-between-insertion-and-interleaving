import random
import unittest
from ordenacao import (
    ordenacao_insercao,
    ordenacao_intercalacao,
    ordenar_sorted_contando,
)


class TestOrdenacao(unittest.TestCase):
    def setUp(self):
        self.algoritmos = [
            ("Inserção", ordenacao_insercao),
            ("Intercalação", ordenacao_intercalacao),
            ("Sorted (com contador)", ordenar_sorted_contando),
        ]

    def test_lista_vazia(self):
        for nome, func in self.algoritmos:
            with self.subTest(algoritmo=nome):
                ordenada, comp = func([])
                self.assertEqual(ordenada, [])
                self.assertEqual(comp, 0)

    def test_um_elemento(self):
        for nome, func in self.algoritmos:
            with self.subTest(algoritmo=nome):
                ordenada, comp = func([42])
                self.assertEqual(ordenada, [42])
                self.assertEqual(comp, 0)

    def test_todos_elementos_iguais(self):
        entrada = [7, 7, 7, 7, 7, 7, 7, 7]
        esperado = [7, 7, 7, 7, 7, 7, 7, 7]
        for nome, func in self.algoritmos:
            with self.subTest(algoritmo=nome):
                ordenada, comp = func(entrada)
                self.assertEqual(ordenada, esperado)
                self.assertGreaterEqual(comp, len(entrada) - 1)

    def test_lista_ja_ordenada(self):
        entrada = list(range(1, 21))
        esperado = list(range(1, 21))
        for nome, func in self.algoritmos:
            with self.subTest(algoritmo=nome):
                ordenada, comp = func(entrada)
                self.assertEqual(ordenada, esperado)
                if nome == "Inserção":
                   
                    self.assertEqual(comp, len(entrada) - 1)

    def test_lista_invertida(self):
        n = 20
        entrada = list(range(n, 0, -1))
        esperado = list(range(1, n + 1))
        for nome, func in self.algoritmos:
            with self.subTest(algoritmo=nome):
                ordenada, comp = func(entrada)
                self.assertEqual(ordenada, esperado)
                if nome == "Inserção":
                   
                    self.assertEqual(comp, n * (n - 1) // 2)

    def test_nao_modifica_lista_original(self):
        original = [5, 2, 9, 1, 5, 6]
        copia = original.copy()
        for nome, func in self.algoritmos:
            with self.subTest(algoritmo=nome):
                func(original)
                self.assertEqual(original, copia)

    def test_listas_aleatorias_com_negativos_e_repetidos(self):
        random.seed(123)
        for _ in range(20):
            tamanho = random.randint(0, 150)
            entrada = [random.randint(-100, 100) for _ in range(tamanho)]
            esperado = sorted(entrada)
            for nome, func in self.algoritmos:
                with self.subTest(algoritmo=nome, tamanho=tamanho):
                    ordenada, _ = func(entrada)
                    self.assertEqual(ordenada, esperado)


if __name__ == "__main__":
    unittest.main(verbosity=2)
