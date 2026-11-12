"""Rotação planar em graus, preservando as dimensões de saída."""
import cv2
import numpy as np


def rotacionar(imagem: np.ndarray, angulo: float) -> np.ndarray:
    if imagem is None or imagem.size == 0:
        raise ValueError("Imagem vazia ou inválida")
    altura, largura = imagem.shape[:2]
    centro = ((largura - 1) / 2.0, (altura - 1) / 2.0)
    matriz = cv2.getRotationMatrix2D(centro, float(angulo), 1.0)
    return cv2.warpAffine(imagem, matriz, (largura, altura))
