from typing import List, Tuple, Any


class ElementoComparavel:
    
    comparacoes: int = 0

    def __init__(self, valor: Any):
        self.valor = valor

    def __lt__(self, outro: "ElementoComparavel") -> bool:
        ElementoComparavel.comparacoes += 1
        return self.valor < outro.valor

    def __eq__(self, outro: object) -> bool:
        if isinstance(outro, ElementoComparavel):
            return self.valor == outro.valor
        return False

    def __repr__(self) -> str:
        return repr(self.valor)


def ordenacao_insercao(lista: List[Any]) -> Tuple[List[Any], int]:
    
    arr = lista.copy()
    comparacoes = 0
    n = len(arr)

    for i in range(1, n):
        chave = arr[i]
        j = i - 1
        while j >= 0:
            comparacoes += 1
            if arr[j] > chave:
                arr[j + 1] = arr[j]
                j -= 1
            else:
                break
        arr[j + 1] = chave

    return arr, comparacoes


def _intercalar(esquerda: List[Any], direita: List[Any]) -> Tuple[List[Any], int]:
   
    resultado = []
    i = 0
    j = 0
    comparacoes = 0
    tam_esq = len(esquerda)
    tam_dir = len(direita)

    while i < tam_esq and j < tam_dir:
        comparacoes += 1
        if esquerda[i] <= direita[j]:
            resultado.append(esquerda[i])
            i += 1
        else:
            resultado.append(direita[j])
            j += 1

    resultado.extend(esquerda[i:])
    resultado.extend(direita[j:])
    return resultado, comparacoes


def ordenacao_intercalacao(lista: List[Any]) -> Tuple[List[Any], int]:
   
    if len(lista) <= 1:
        return lista.copy(), 0

    meio = len(lista) // 2
    esquerda, comp_esq = ordenacao_intercalacao(lista[:meio])
    direita, comp_dir = ordenacao_intercalacao(lista[meio:])
    intercalada, comp_inter = _intercalar(esquerda, direita)

    return intercalada, comp_esq + comp_dir + comp_inter


def ordenar_sorted_contando(lista: List[Any]) -> Tuple[List[Any], int]:
   
    ElementoComparavel.comparacoes = 0
    encapsulada = [ElementoComparavel(x) for x in lista]
    ordenada = sorted(encapsulada)
    return [x.valor for x in ordenada], ElementoComparavel.comparacoes
