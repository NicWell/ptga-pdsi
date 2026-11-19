"""Demonstração sintética reproduzível; não depende de imagens externas."""
import json
from pathlib import Path

import cv2
import numpy as np

from .alinhamento import alinhar
from .espelhamento import espelhar
from .redimensionamento import redimensionar
from .rotacao import rotacionar
from .translacao import transladar


def criar_cena() -> np.ndarray:
    """Cena assimétrica BGR de 320 × 320, com textura e marcas reconhecíveis."""
    rng = np.random.default_rng(2026)
    cinza = rng.integers(20, 90, (320, 320), dtype=np.uint8)
    cena = cv2.cvtColor(cinza, cv2.COLOR_GRAY2BGR)
    for _ in range(100):
        x, y = rng.integers(15, 305, 2)
        cor = tuple(int(c) for c in rng.integers(100, 256, 3))
        cv2.circle(cena, (int(x), int(y)), int(rng.integers(2, 7)), cor, -1)
    cv2.rectangle(cena, (30, 40), (110, 105), (40, 180, 240), -1)
    cv2.circle(cena, (245, 80), 32, (220, 160, 30), -1)
    cv2.arrowedLine(cena, (60, 250), (220, 170), (80, 240, 100), 8)
    cv2.putText(cena, 'PDSI 2026', (25, 300), cv2.FONT_HERSHEY_SIMPLEX,
                0.85, (255, 255, 255), 2, cv2.LINE_AA)
    return cena


def montar_painel(itens: list[tuple[str, np.ndarray]], colunas: int = 2) -> np.ndarray:
    """Centraliza imagens no tamanho nativo; não reamostra os resultados."""
    if not itens or colunas < 1:
        raise ValueError('Informe imagens e um número positivo de colunas')
    largura = max(max(img.shape[1] for _, img in itens), 320) + 24
    altura = max(img.shape[0] for _, img in itens) + 68
    linhas = (len(itens) + colunas - 1) // colunas
    painel = np.full((linhas * altura, colunas * largura, 3), 245, dtype=np.uint8)
    for i, (titulo, img) in enumerate(itens):
        y, x = (i // colunas) * altura, (i % colunas) * largura
        cv2.putText(painel, titulo, (x + 12, y + 23), cv2.FONT_HERSHEY_SIMPLEX,
                    0.48, (30, 30, 30), 1, cv2.LINE_AA)
        cv2.putText(painel, f'{img.shape[1]} x {img.shape[0]} px',
                    (x + 12, y + 43), cv2.FONT_HERSHEY_SIMPLEX,
                    0.4, (70, 70, 70), 1, cv2.LINE_AA)
        px = x + (largura - img.shape[1]) // 2
        py = y + 56
        painel[py:py + img.shape[0], px:px + img.shape[1]] = img
    return painel


def gerar_demonstracao(destino: str | Path) -> dict:
    """Salva entradas, saídas, painéis e medições do par sintético conhecido."""
    destino = Path(destino)
    destino.mkdir(parents=True, exist_ok=True)

    def salvar(nome, imagem):
        if not cv2.imwrite(str(destino / nome), imagem):
            raise OSError(f'Falha ao salvar: {destino / nome}')

    cena = criar_cena()
    salvar('original.png', cena)
    operacoes = {
        'rotacao': ('Rotacao +30 graus | linear', rotacionar(cena, 30)),
        'translacao': ('Translacao dx=40 dy=-25 | linear', transladar(cena, 40, -25)),
        'espelho_horizontal': ('Espelho horizontal', espelhar(cena, 'horizontal')),
        'espelho_vertical': ('Espelho vertical', espelhar(cena, 'vertical')),
        'espelho_ambos': ('Espelho ambos', espelhar(cena, 'ambos')),
    }
    for nome, (titulo, resultado) in operacoes.items():
        salvar(f'{nome}.png', resultado)
        salvar(f'comparacao_{nome}.png', montar_painel([('Original', cena), (titulo, resultado)]))

    itens = []
    for metodo in ('nearest', 'linear', 'cubic', 'area'):
        resultado = redimensionar(cena, 137, 137, metodo)
        salvar(f'redimensionamento_{metodo}.png', resultado)
        itens.append((f'Reducao 320 -> 137 | {metodo}', resultado))
    salvar('comparacao_redimensionamento.png', montar_painel([('Original', cena), *itens]))
    # Mesmo recorte ampliado por nearest apenas para inspecionar os pixels da redução.
    salvar('detalhe_interpolacoes.png', montar_painel([
        (titulo, np.repeat(np.repeat(img[15:55, 15:55], 6, axis=0), 6, axis=1))
        for titulo, img in itens
    ]))

    # Movimento conhecido independente do módulo de translação: +12 em x e -8 em y.
    movel = np.zeros_like(cena)
    movel[:312, 12:] = cena[8:, :308]
    cv2.setRNGSeed(2026)
    alinhada = alinhar(cena, movel)
    salvar('movel.png', movel)
    salvar('alinhada.png', alinhada)
    salvar('comparacao_alinhamento.png', montar_painel([
        ('Referencia', cena), ('Movel dx=12 dy=-8', movel),
        ('Alinhada ORB + RANSAC', alinhada),
        ('Sobreposicao referencia/alinhada 50%', cv2.addWeighted(cena, 0.5, alinhada, 0.5, 0)),
    ]))
    regiao = np.s_[32:-32, 32:-32]

    def mae(img):
        return float(np.mean(np.abs(img[regiao].astype(float) - cena[regiao])))

    sem_textura = np.zeros_like(cena)
    salvar('sem_textura.png', sem_textura)
    try:
        alinhar(sem_textura, sem_textura)
    except ValueError as exc:
        falha = str(exc)
    else:
        raise RuntimeError('O caso sem textura deveria rejeitar o alinhamento')
    resumo = {
        'cenario': 'Sintetico; semente 2026; nao representa validacao em imagens reais',
        'numpy': np.__version__, 'opencv': cv2.__version__,
        'movimento_referencia_para_movel': {'dx': 12, 'dy': -8},
        'regiao_avaliada': 'y=32:288, x=32:288; tres canais BGR',
        'mae_antes': mae(movel), 'mae_depois': mae(alinhada),
        'falha_sem_textura': falha,
    }
    (destino / 'resumo.json').write_text(json.dumps(resumo, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return resumo
