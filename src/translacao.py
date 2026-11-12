"""Translação com deslocamentos em pixels; pixels fora da imagem são descartados."""
import cv2
import numpy as np


def transladar(imagem: np.ndarray, dx: float, dy: float) -> np.ndarray:
    if imagem is None or imagem.size == 0:
        raise ValueError("Imagem vazia ou inválida")
    altura, largura = imagem.shape[:2]
    matriz = np.float32([[1, 0, dx], [0, 1, dy]])
    return cv2.warpAffine(imagem, matriz, (largura, altura))
