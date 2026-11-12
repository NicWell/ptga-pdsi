"""Espelhamento horizontal, vertical ou ambos."""
import cv2
import numpy as np

CODIGOS = {"horizontal": 1, "vertical": 0, "ambos": -1}


def espelhar(imagem: np.ndarray, eixo: str = "horizontal") -> np.ndarray:
    if imagem is None or imagem.size == 0:
        raise ValueError("Imagem vazia ou inválida")
    if eixo not in CODIGOS:
        raise ValueError(f"Eixo inválido: {eixo}")
    return cv2.flip(imagem, CODIGOS[eixo])
