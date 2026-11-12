import numpy as np
import pytest
from src.rotacao import rotacionar
from src.translacao import transladar
from src.espelhamento import espelhar
from src.redimensionamento import redimensionar
from src.alinhamento import alinhar


def imagem():
    arr = np.zeros((10, 12, 3), dtype=np.uint8)
    arr[2, 3] = [255, 120, 30]
    return arr


def test_rotacao_zero():
    assert np.array_equal(rotacionar(imagem(), 0), imagem())


def test_translacao():
    saida = transladar(imagem(), 2, 1)
    assert np.array_equal(saida[3, 5], imagem()[2, 3])


def test_espelhamento_horizontal():
    assert np.array_equal(espelhar(imagem(), "horizontal")[:, -1], imagem()[:, 0])


def test_redimensionamento():
    assert redimensionar(imagem(), 24, 20).shape == (20, 24, 3)


def test_dimensoes_invalidas():
    with pytest.raises(ValueError): redimensionar(imagem(), 0, 20)


def test_alinhamento_sem_textura():
    with pytest.raises(ValueError): alinhar(np.zeros((60, 60), dtype=np.uint8), np.zeros((60, 60), dtype=np.uint8))
