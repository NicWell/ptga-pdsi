# Transformações Geométricas e Alinhamento de Imagens

Projeto acadêmico da disciplina **Processamento Digital de Sinais e Imagens** (PDSI).

**Equipe:** Vitória Regina dos Santos Melo, Antônio Elvis Pinheiro Nascimento da Silva e Wellington Nicacio Gama Canuto.

## Escopo

- Rotação, translação, espelhamento e redimensionamento de imagens.
- Registro/alinhamento de duas imagens com ORB, correspondência de descritores, RANSAC e homografia (protótipo sujeito a testes).
- Comparação da imagem de entrada com os resultados.

Os requisitos originais do professor são Python, OpenCV, operações geométricas e alinhamento, dataset COCO **sugerido**, apresentação de acompanhamento e apresentação final de **10–15 min** cada, além de apresentação e repositório. A interface gráfica é opcional.

## Preparação (Windows PowerShell)

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Se a política de execução impedir a ativação, use diretamente ` .\.venv\Scripts\python.exe ` em vez de ativar a venv.

## Execução

Para gerar todos os exemplos sintéticos e comparações sem baixar imagens:

```powershell
python app.py demonstracao
```

Abra os painéis `comparacao_*.png` em `resultados/demonstracao/`.
O [guia da demonstração](docs/DEMONSTRACAO.md) explica o conteúdo e as limitações.
O acompanhamento foi confirmado pelo integrante para **19/11/2026**.

```powershell
python app.py rotacao --entrada caminho/para/imagem.jpg --angulo 30 --saida resultados/rotacionada.png
python app.py translacao --entrada caminho/para/imagem.jpg --dx 80 --dy 30 --saida resultados/transladada.png
python app.py espelhamento --entrada caminho/para/imagem.jpg --eixo horizontal --saida resultados/espelhada.png
python app.py redimensionamento --entrada caminho/para/imagem.jpg --largura 640 --altura 480 --saida resultados/redimensionada.png
python app.py alinhamento --referencia caminho/para/ref.jpg --movel caminho/para/movel.jpg --saida resultados/alinhada.png
python -m pytest -q
```

O comando de alinhamento necessita duas imagens da mesma cena, com sobreposição e pontos característicos suficientes. Caso não haja correspondências adequadas, o script informa o erro.

Para reproduzir o experimento com duas fotografias do COCO val2014, coloque os
originais indicados no [catálogo](imagens/catalogo.json) em `imagens/originais/`
e execute:

```powershell
python -m src.experimento_coco
```

O comando gera os painéis e o resumo em `resultados/coco/`. Consulte os
[resultados e o procedimento](imagens/README.md#reproduzir-o-teste-com-o-coco-val2014).

## Organização

- `src/`: implementações reutilizáveis.
- `app.py`: interface inicial por linha de comando (CLI).
- `tests/`: testes automatizados sintéticos.
- `imagens/`: [banco local e catálogo de amostras](imagens/README.md); as mídias são **não versionadas** por padrão.
- `resultados/`: saídas geradas, não versionadas.
- `docs/`: contexto, metodologia e acompanhamento.
- `AGENTS.md`: instruções de trabalho para o Codex.

## Situação atual

Os testes sintéticos cobrem transformações conhecidas, formatos cinza/BGR/BGRA
nas operações básicas e alinhamento de translações conhecidas. Consulte a
[metodologia e os limites dos testes](docs/TESTES_SINTETICOS.md).

**Protótipo funcional:** operações geométricas, alinhamento pela CLI,
demonstração sintética e experimento local com duas amostras COCO val2014.
Nos quatro pares controlados, o erro absoluto médio caiu após o alinhamento.
O controle com cenas distintas foi rejeitado. A validação com duas capturas
sobrepostas da mesma cena segue pendente.

O guia do código atualizado com o experimento COCO fica localmente em
`output/pdf/guia-do-codigo-pdsi.pdf`. O Git ignora esse diretório.

## Próximas entregas

1. Retomar em outra sessão a avaliação de um par de capturas sobrepostas da mesma cena.
2. Ampliar a suíte automatizada de alinhamento para rotação, perspectiva e homografias degeneradas.
3. Medir tempo e erro de reprojeção com um procedimento reproduzível, como complemento ao MAE já registrado.
4. Consolidar as evidências na apresentação final de 10–15 minutos e no repositório.

Consulte [`CONTEXTO_PROJETO.md`](CONTEXTO_PROJETO.md) para decisões, integrantes, fontes e histórico, e [`AGENTS.md`](AGENTS.md) para orientar assistência por IA.
