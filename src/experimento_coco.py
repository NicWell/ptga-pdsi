"""Avaliação local das duas amostras COCO val2014 do catálogo."""

import json
from pathlib import Path

import cv2
import numpy as np

from .alinhamento import alinhar
from .demonstracao import montar_painel
from .espelhamento import espelhar
from .redimensionamento import redimensionar
from .rotacao import rotacionar
from .translacao import transladar


def salvar(caminho, imagem):
    if not cv2.imwrite(str(caminho), imagem):
        raise OSError(f"Falha ao salvar {caminho}")


def avaliar_par(referencia, movel, matriz, pasta, nome):
    h, w = referencia.shape[:2]
    tamanho = (w, h)
    # Seleciona pixels que permanecem no quadro após o movimento e sua inversa.
    mascara = np.full((h, w), 255, dtype=np.uint8)
    mascara_movel = cv2.warpPerspective(mascara, matriz, tamanho, flags=cv2.INTER_NEAREST)
    comum = cv2.warpPerspective(
        mascara_movel, np.linalg.inv(matriz), tamanho, flags=cv2.INTER_NEAREST
    )
    regiao = cv2.erode(comum, np.ones((5, 5), dtype=np.uint8)) == 255
    salvar(pasta / f"{nome}_movel.png", movel)
    resumo = {
        "matriz_referencia_para_movel": matriz.tolist(),
        "pixels_avaliados": int(regiao.sum()),
        "mae_antes": float(np.abs(movel[regiao].astype(float) - referencia[regiao]).mean()),
    }
    cv2.setRNGSeed(2026)
    try:
        alinhada = alinhar(referencia, movel)
    except ValueError as erro:
        return {**resumo, "status": "rejeitado", "mensagem": str(erro)}
    salvar(pasta / f"{nome}_alinhada.png", alinhada)
    salvar(pasta / f"{nome}_comparacao.png", montar_painel([
        ("Referencia", referencia), ("Movel", movel), ("Alinhada", alinhada),
        ("Sobreposicao 50%", cv2.addWeighted(referencia, 0.5, alinhada, 0.5, 0)),
    ]))
    return {
        **resumo, "status": "aceito",
        "mae_depois": float(np.abs(alinhada[regiao].astype(float) - referencia[regiao]).mean()),
    }


def executar():
    raiz = Path(__file__).resolve().parents[1]
    destino = raiz / "resultados" / "coco"
    originais = {}
    for id_imagem in ("000000019221", "000000044652"):
        caminho = raiz / "imagens" / "originais" / f"{id_imagem}.jpg"
        imagem = cv2.imread(str(caminho), cv2.IMREAD_COLOR)
        if imagem is None:
            raise ValueError(f"Não foi possível abrir {caminho}")
        originais[id_imagem] = imagem

    resumo = {"opencv": cv2.__version__, "numpy": np.__version__, "amostras": {}}
    for id_imagem, imagem in originais.items():
        pasta = destino / id_imagem
        pasta.mkdir(parents=True, exist_ok=True)
        h, w = imagem.shape[:2]
        rodada = rotacionar(imagem, 15)
        operacoes = [
            ("Rotacao +15 graus", rodada),
            ("Translacao dx=40 dy=-25", transladar(imagem, 40, -25)),
            ("Espelho horizontal", espelhar(imagem)),
            ("Reducao 50% | area", redimensionar(imagem, w // 2, h // 2, "area")),
        ]
        salvar(pasta / "transformacoes.png", montar_painel([("Original", imagem), *operacoes]))
        matriz_rotacao = np.vstack([
            cv2.getRotationMatrix2D(((w - 1) / 2, (h - 1) / 2), 15, 1), [0, 0, 1],
        ])
        cantos = np.float32([[0, 0], [w-1, 0], [w-1, h-1], [0, h-1]])
        recuo = np.float32([[.04*w, .05*h], [-.06*w, .02*h], [-.02*w, -.05*h], [.03*w, -.02*h]])
        perspectiva = cv2.getPerspectiveTransform(cantos, cantos + recuo)
        resumo["amostras"][id_imagem] = {
            "largura": w, "altura": h,
            "rotacao": avaliar_par(imagem, rodada, matriz_rotacao, pasta, "rotacao"),
            "perspectiva": avaliar_par(
                imagem, cv2.warpPerspective(imagem, perspectiva, (w, h)),
                perspectiva, pasta, "perspectiva",
            ),
        }

    referencia, movel = originais.values()
    cv2.setRNGSeed(2026)
    try:
        alinhar(referencia, movel)
    except ValueError as erro:
        resumo["cenas_distintas"] = {"status": "rejeitado", "mensagem": str(erro)}
    else:
        resumo["cenas_distintas"] = {"status": "aceito", "mensagem": "Falso positivo"}
    (destino / "resumo.json").write_text(
        json.dumps(resumo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Resultados salvos em {destino}")


if __name__ == "__main__":
    executar()
