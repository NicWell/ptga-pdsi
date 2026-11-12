"""Protótipo de alinhamento por ORB, matching Hamming e homografia RANSAC."""
import cv2
import numpy as np


def alinhar(referencia: np.ndarray, movel: np.ndarray, minimo_correspondencias: int = 10) -> np.ndarray:
    """Retorna a imagem móvel alinhada às dimensões da referência.

    Requer cena comum e textura suficiente. Falhas são informadas por ValueError.
    """
    if referencia is None or movel is None or referencia.size == 0 or movel.size == 0:
        raise ValueError("Imagens inválidas")
    if minimo_correspondencias < 4:
        raise ValueError("Mínimo de correspondências deve ser >= 4")
    def cinza(img):
        if img.ndim == 2:
            return img
        if img.ndim == 3 and img.shape[2] == 3:
            return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        if img.ndim == 3 and img.shape[2] == 4:
            return cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        raise ValueError("Formato de imagem não suportado")

    orb = cv2.ORB_create(nfeatures=2000)
    pontos_m, desc_m = orb.detectAndCompute(cinza(movel), None)
    pontos_r, desc_r = orb.detectAndCompute(cinza(referencia), None)
    if desc_m is None or desc_r is None:
        raise ValueError("Pontos característicos insuficientes para alinhamento")
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    pares = matcher.knnMatch(desc_m, desc_r, k=2)
    bons = [a for par in pares if len(par) == 2 for a, b in [par] if a.distance < 0.75 * b.distance]
    if len(bons) < minimo_correspondencias:
        raise ValueError(f"Correspondências insuficientes: {len(bons)}")
    origem = np.float32([pontos_m[m.queryIdx].pt for m in bons]).reshape(-1, 1, 2)
    destino = np.float32([pontos_r[m.trainIdx].pt for m in bons]).reshape(-1, 1, 2)
    homografia, mascara = cv2.findHomography(origem, destino, cv2.RANSAC, 4.0)
    if homografia is None or mascara is None or int(mascara.sum()) < 4:
        raise ValueError("Falha ao estimar homografia confiável")
    altura, largura = referencia.shape[:2]
    return cv2.warpPerspective(movel, homografia, (largura, altura))
