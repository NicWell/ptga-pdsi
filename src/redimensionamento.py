"""Redimensionamento com interpolação configurável."""
import cv2
import numpy as np

INTERPOLACOES = {"nearest": cv2.INTER_NEAREST, "linear": cv2.INTER_LINEAR, "cubic": cv2.INTER_CUBIC, "area": cv2.INTER_AREA}


def redimensionar(imagem: np.ndarray, largura: int, altura: int, interpolacao: str = "linear") -> np.ndarray:
    if imagem is None or imagem.size == 0:
        raise ValueError("Imagem vazia ou inválida")
    if largura <= 0 or altura <= 0:
        raise ValueError("Largura e altura devem ser positivas")
    if interpolacao not in INTERPOLACOES:
        raise ValueError(f"Interpolação inválida: {interpolacao}")
    return cv2.resize(imagem, (largura, altura), interpolation=INTERPOLACOES[interpolacao])
