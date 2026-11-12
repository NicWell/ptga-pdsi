"""Testes sintéticos com resultados conhecidos, sem arquivos externos."""
import numpy as np
import pytest
from src.rotacao import rotacionar
from src.translacao import transladar
from src.espelhamento import espelhar
from src.redimensionamento import redimensionar


@pytest.fixture(params=[None, 3, 4], ids=['cinza', 'BGR', 'BGRA'])
def imagem(request):
    shape = (5, 5) if request.param is None else (5, 5, request.param)
    return np.arange(np.prod(shape), dtype=np.uint8).reshape(shape)


@pytest.mark.parametrize('angulo,k', [(0, 0), (90, 1), (-90, -1), (180, 2), (360, 0)])
def test_rotacao_conhecida(imagem, angulo, k):
    np.testing.assert_array_equal(rotacionar(imagem, angulo), np.rot90(imagem, k))


@pytest.mark.parametrize('dx,dy', [(0, 0), (2, 1), (-2, -1), (1, -2), (5, 0), (0, -5)])
def test_translacao_e_bordas(imagem, dx, dy):
    esperado = np.zeros_like(imagem)
    for y in range(5):
        for x in range(5):
            if 0 <= x + dx < 5 and 0 <= y + dy < 5:
                esperado[y + dy, x + dx] = imagem[y, x]
    np.testing.assert_array_equal(transladar(imagem, dx, dy), esperado)


def test_translacao_fracionaria_linear():
    entrada = np.array([[0, 80, 160, 240]], dtype=np.uint8)
    np.testing.assert_array_equal(transladar(entrada, 0.5, 0), [[0, 40, 120, 200]])


@pytest.mark.parametrize('eixo,axes', [('horizontal', 1), ('vertical', 0), ('ambos', (0, 1))])
def test_espelhamento_completo(imagem, eixo, axes):
    np.testing.assert_array_equal(espelhar(imagem, eixo), np.flip(imagem, axis=axes))


@pytest.mark.parametrize('metodo', ['nearest', 'linear', 'cubic', 'area'])
def test_redimensionamento_identidade(imagem, metodo):
    np.testing.assert_array_equal(redimensionar(imagem, 5, 5, metodo), imagem)


def test_ampliacao_nearest(imagem):
    esperado = np.repeat(np.repeat(imagem, 2, axis=0), 2, axis=1)
    np.testing.assert_array_equal(redimensionar(imagem, 10, 10, 'nearest'), esperado)


@pytest.mark.parametrize('metodo', ['linear', 'area'])
def test_reducao_media_conhecida(metodo):
    entrada = np.array([[0, 40, 80, 120], [40, 80, 120, 160]], dtype=np.uint8)
    np.testing.assert_array_equal(redimensionar(entrada, 2, 1, metodo), [[40, 120]])


@pytest.mark.parametrize('metodo', ['nearest', 'linear', 'cubic', 'area'])
def test_redimensionamento_constante(metodo):
    entrada = np.full((3, 5, 3), [20, 80, 160], dtype=np.uint8)
    saida = redimensionar(entrada, 9, 7, metodo)
    assert saida.dtype == entrada.dtype
    np.testing.assert_array_equal(saida, np.full((7, 9, 3), [20, 80, 160], dtype=np.uint8))


@pytest.mark.parametrize('largura,altura', [(0, 5), (5, 0), (-1, 5), (5, -1)])
def test_dimensoes_invalidas(largura, altura):
    with pytest.raises(ValueError, match='positivas'):
        redimensionar(np.zeros((3, 3), dtype=np.uint8), largura, altura)


def test_opcoes_invalidas(imagem):
    with pytest.raises(ValueError, match='Eixo'):
        espelhar(imagem, 'diagonal')
    with pytest.raises(ValueError, match='Interpola'):
        redimensionar(imagem, 5, 5, 'inexistente')


@pytest.mark.parametrize('entrada', [None, np.empty((0, 5), dtype=np.uint8)])
@pytest.mark.parametrize('operacao,args', [
    (rotacionar, (30,)), (transladar, (1, 1)),
    (espelhar, ()), (redimensionar, (3, 3)),
])
def test_imagens_invalidas(entrada, operacao, args):
    with pytest.raises(ValueError, match='Imagem vazia'):
        operacao(entrada, *args)


def test_entrada_preservada(imagem):
    original = imagem.copy()
    rotacionar(imagem, 30)
    transladar(imagem, 1, -1)
    espelhar(imagem)
    redimensionar(imagem, 7, 3)
    np.testing.assert_array_equal(imagem, original)
