"""Verifica a demonstração pela CLI, incluindo imagens e medições salvas."""
import json
from pathlib import Path
import subprocess
import sys

import cv2
import numpy as np


def test_cli_demonstracao(tmp_path):
    destino = tmp_path / 'demo'
    raiz = Path(__file__).resolve().parents[1]
    processo = subprocess.run(
        [sys.executable, str(raiz / 'app.py'), 'demonstracao', '--destino', str(destino)],
        cwd=tmp_path, capture_output=True, text=True, timeout=30,
    )
    assert processo.returncode == 0, processo.stderr
    resumo = json.loads((destino / 'resumo.json').read_text(encoding='utf-8'))
    assert resumo['mae_depois'] < resumo['mae_antes'] * 0.25
    assert 'insuficientes' in resumo['falha_sem_textura']
    referencia = cv2.imread(str(destino / 'original.png'))
    alinhada = cv2.imread(str(destino / 'alinhada.png'))
    regiao = np.s_[32:-32, 32:-32]
    medido = np.mean(np.abs(alinhada[regiao].astype(float) - referencia[regiao]))
    assert resumo['mae_depois'] == float(medido)
    esperados = [
        'comparacao_rotacao.png', 'comparacao_translacao.png',
        'comparacao_espelho_horizontal.png', 'comparacao_espelho_vertical.png',
        'comparacao_espelho_ambos.png', 'comparacao_redimensionamento.png',
        'detalhe_interpolacoes.png', 'comparacao_alinhamento.png',
    ]
    for nome in esperados:
        img = cv2.imread(str(destino / nome))
        assert img is not None, nome
        assert img.shape[0] > 320 and img.shape[1] > 640, nome
