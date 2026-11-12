"""Registro ORB/RANSAC real em textura sintética com semente fixa."""
import cv2
import numpy as np
import pytest
from src.alinhamento import alinhar


@pytest.fixture
def textura():
    # Dimensão suficiente para pontos ORB longe da margem de exclusão.
    return np.random.default_rng(2026).integers(0, 256, (256, 256), dtype=np.uint8)


@pytest.mark.parametrize('dx,dy', [(0, 0), (8, -6), (-7, 5)])
def test_recupera_translacao(textura, dx, dy):
    cv2.setRNGSeed(2026)
    movel = np.zeros_like(textura)
    # Construção por índices, independente das funções do projeto.
    for y in range(256):
        for x in range(256):
            if 0 <= x + dx < 256 and 0 <= y + dy < 256:
                movel[y + dy, x + dx] = textura[y, x]
    original = movel.copy()
    alinhada = alinhar(textura, movel)
    assert alinhada.shape == textura.shape
    assert alinhada.dtype == textura.dtype
    regiao = np.s_[32:-32, 32:-32]
    erro = np.mean(np.abs(alinhada[regiao].astype(float) - textura[regiao]))
    assert erro < 15, f'Erro absoluto médio na região comum: {erro:.2f}'
    if dx or dy:
        antes = np.mean(np.abs(movel[regiao].astype(float) - textura[regiao]))
        assert erro < antes * 0.25
    np.testing.assert_array_equal(movel, original)


@pytest.mark.parametrize('lado', ['referencia', 'movel'])
@pytest.mark.parametrize('entrada', [None, np.empty((0, 5), dtype=np.uint8)])
def test_imagem_invalida(textura, lado, entrada):
    imagens = {'referencia': textura, 'movel': textura}
    imagens[lado] = entrada
    with pytest.raises(ValueError, match='Imagens inv'):
        alinhar(**imagens)


@pytest.mark.parametrize('lado', ['referencia', 'movel'])
def test_sem_textura(textura, lado):
    imagens = {'referencia': textura, 'movel': textura}
    imagens[lado] = np.zeros_like(textura)
    with pytest.raises(ValueError, match='Pontos caracter'):
        alinhar(**imagens)


def test_minimo_invalido(textura):
    with pytest.raises(ValueError, match='>= 4'):
        alinhar(textura, textura, minimo_correspondencias=3)


def test_correspondencias_insuficientes(textura):
    with pytest.raises(ValueError, match='Correspond'):
        alinhar(textura, textura, minimo_correspondencias=10000)


def test_formato_nao_suportado(textura):
    with pytest.raises(ValueError, match='Formato de imagem'):
        alinhar(textura, np.zeros((256, 256, 2), dtype=np.uint8))
