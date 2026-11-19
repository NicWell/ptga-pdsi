# Demonstração para o acompanhamento de 19/11/2026

A data foi confirmada pelo integrante. Este guia é uma proposta de demonstração
da equipe; não acrescenta exigências do professor. Não é um conjunto de slides.

## Gerar as evidências

Na raiz do repositório, com o ambiente ativado:

```powershell
python app.py demonstracao
```

Sem ativar a venv: `.\.venv\Scripts\python.exe app.py demonstracao`.
Para outro diretório: `python app.py demonstracao --destino resultados/ensaio`.
A rotina pode ser repetida; substitui os arquivos de mesmos nomes no destino.
Não há download nem janela gráfica obrigatória. As imagens são geradas pelo
código do projeto, sem material externo. As saídas continuam ignoradas pelo Git.

## O que mostrar

1. `comparacao_rotacao.png`: +30°, centro (159,5; 159,5), quadro 320 × 320.
   Matriz 2 × 3 de `getRotationMatrix2D`; interpolação linear; bordas pretas.
   O corte é consequência de manter as dimensões, não de perder o arquivo.
2. `comparacao_translacao.png`: dx=40 e dy=-25 pixels. Matriz
   `[[1, 0, 40], [0, 1, -25]]`; x cresce para a direita e y para baixo.
   Interpolação linear e bordas pretas; conteúdo fora do quadro é descartado.
3. `comparacao_espelho_*.png`: horizontal, vertical e ambos. Para largura W e
   altura H: x'=W-1-x e/ou y'=H-1-y. Não há interpolação: os pixels são permutados.
4. `comparacao_redimensionamento.png`: redução de 320 × 320 para 137 × 137,
   escala 137/320 nos dois eixos. Os métodos selecionados são nearest (vizinho
   mais próximo), linear (bilinear), cubic (bicúbica) e area (média de área).
   Os resultados são exibidos no tamanho nativo, sem esticá-los para comparação.
   Em `detalhe_interpolacoes.png`, o mesmo recorte de cada saída foi ampliado
   6 vezes por repetição de pixels, apenas para inspeção dos métodos de redução.
5. `comparacao_alinhamento.png`: referência, móvel deslocada +12/-8 pixels,
   imagem alinhada e sobreposição 50%. ORB detecta pontos, Hamming associa
   descritores, o filtro de razão usa 0,75 e RANSAC estima a homografia 3 × 3
   da móvel para a referência (limiar de reprojeção de 4 pixels).
   `warpPerspective` usa interpolação linear e bordas pretas.
6. `resumo.json`: mostra a falha esperada sem textura e o MAE antes/depois.
   `sem_textura.png` permite repetir essa falha pela CLI original.

## Reproduzir operações individuais

```powershell
python app.py rotacao --entrada resultados/demonstracao/original.png --angulo 30 --saida resultados/ao_vivo.png
python app.py alinhamento --referencia resultados/demonstracao/original.png --movel resultados/demonstracao/movel.png --saida resultados/alinhamento_ao_vivo.png
python app.py alinhamento --referencia resultados/demonstracao/sem_textura.png --movel resultados/demonstracao/sem_textura.png --saida resultados/falha.png
```

O último comando deve terminar com código 1 e mensagem de pontos insuficientes,
sem criar um resultado de alinhamento.

## Medição e limites

A cena usa semente NumPy 2026 e o RANSAC recebe semente OpenCV 2026.
MAE é a média de `abs(alinhada - referencia)` nos três canais BGR, após conversão
para float. Usa-se a região x=32:288, y=32:288, excluindo as bordas perdidas.
As unidades são níveis de intensidade de 0 a 255. Não se mede o desempenho
temporal, nem se afirma que a homografia serve para qualquer cena.

Na execução local de 12/11/2026, OpenCV 4.14.0 e NumPy 2.5.4, o MAE passou
de aproximadamente **40,39 para 1,97**. O JSON contém os valores completos
medidos em cada execução. Pequenas diferenças entre versões são possíveis.

Há apenas um par demonstrativo por translação; os testes usam outros
deslocamentos. Rotação e perspectiva no registro, cenas sem sobreposição,
casos degenerados e fotografias reais ainda precisam de validação.

## Preparação restante

- Selecionar fotografias próprias ou imagens com licença e origem registradas.
- Preparar slides para 10–15 minutos com objetivo, matrizes, exemplos e limites.
- Ensaiar com a equipe até 18/11 (meta interna sugerida), mantendo os painéis
  previamente gerados disponíveis para o acompanhamento em 19/11.
