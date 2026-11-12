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

```powershell
python app.py rotacao --entrada caminho/para/imagem.jpg --angulo 30 --saida resultados/rotacionada.png
python app.py translacao --entrada caminho/para/imagem.jpg --dx 80 --dy 30 --saida resultados/transladada.png
python app.py espelhamento --entrada caminho/para/imagem.jpg --eixo horizontal --saida resultados/espelhada.png
python app.py redimensionamento --entrada caminho/para/imagem.jpg --largura 640 --altura 480 --saida resultados/redimensionada.png
python app.py alinhamento --referencia caminho/para/ref.jpg --movel caminho/para/movel.jpg --saida resultados/alinhada.png
python -m pytest -q
```

O comando de alinhamento necessita duas imagens da mesma cena, com sobreposição e pontos característicos suficientes. Caso não haja correspondências adequadas, o script informa o erro. Ele ainda precisa de validação com dataset e experimentos; não é garantia de registro em todos os cenários.

## Organização

- `src/`: implementações reutilizáveis.
- `app.py`: interface inicial por linha de comando (CLI).
- `tests/`: testes automatizados sintéticos.
- `imagens/`: amostras locais **não versionadas** por padrão; registrar origem/licença dos datasets.
- `resultados/`: saídas geradas, não versionadas.
- `docs/`: contexto, metodologia e acompanhamento.
- `AGENTS.md`: instruções de trabalho para o Codex.

## Situação atual

Os testes sintéticos cobrem transformações conhecidas, formatos cinza/BGR/BGRA
nas operações básicas e alinhamento de translações conhecidas. Consulte a
[metodologia e os limites dos testes](docs/TESTES_SINTETICOS.md).

**Starter funcional**: operações geométricas e protótipo de alinhamento CLI; não há interface gráfica, dataset baixado, slides, relatório final ou métricas de avaliação completas. Não apresentar essas etapas como concluídas.

## Próximas entregas

1. Escolher imagens do COCO ou de testes próprios, documentando fontes.
2. Verificar saídas visualmente e salvar comparações lado a lado.
3. Testar alinhamento em transformações conhecidas e reportar falhas.
4. Medir tempo, reprojeção/erros com critérios explicitados.
5. Preparar apresentação de acompanhamento (10–15 min) e final (10–15 min).

Consulte [`CONTEXTO_PROJETO.md`](CONTEXTO_PROJETO.md) para decisões, integrantes, fontes e histórico, e [`AGENTS.md`](AGENTS.md) para orientar assistência por IA.
