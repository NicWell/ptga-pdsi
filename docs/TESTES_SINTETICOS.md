# Testes sintéticos

Estes testes são uma estratégia de validação da equipe, não uma exigência
adicional do professor. Não dependem de dataset, imagens externas ou downloads.

## Execução

Na raiz do projeto, com as dependências instaladas:

```powershell
python -m pytest -q
```

Sem ativar o ambiente virtual no Windows:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

## Transformações básicas

- Matrizes assimétricas de 5 × 5 pixels, com valores distintos, em cinza,
  BGR e BGRA. As comparações verificam a imagem inteira.
- Rotações de 0°, 90°, -90°, 180° e 360°, comparadas com `numpy.rot90`.
  O quadro quadrado evita ambiguidade de corte nessas rotações.
- Translações inteiras nos dois sentidos e saída completa do quadro,
  comparadas com posições calculadas por índices e bordas pretas.
  Uma translação de meio pixel verifica a interpolação linear com valores conhecidos.
- Espelhamentos horizontal, vertical e ambos, comparados com `numpy.flip`.
- Redimensionamento: identidade nos quatro métodos; repetição exata de pixels
  com nearest; média conhecida na redução com linear e area; preservação de
  cor constante, dimensões e tipo nos quatro métodos.
- Rejeição de imagens nulas/vazias, dimensões não positivas e opções inválidas;
  preservação da imagem de entrada.

Rotação e translação usam matrizes afins 2 × 3, interpolação linear e bordas
constantes pretas pelos padrões atuais do OpenCV. O redimensionamento seleciona
explicitamente a interpolação. O espelhamento apenas permuta pixels.

## Alinhamento

Uma textura uint8 de 256 × 256 pixels é gerada com `default_rng(2026)`.
Essa dimensão permite detectar pontos ORB fora da margem de exclusão do detector.
As imagens móveis são construídas por índices, sem usar as funções do projeto:
identidade e translações de (8, -6) e (-7, 5) pixels.

O teste executa ORB, associação e RANSAC reais, com semente OpenCV 2026.
A homografia 3 × 3 estimada leva a imagem móvel ao quadro da referência;
`warpPerspective` usa interpolação linear e bordas constantes pretas por padrão.

O erro absoluto médio é calculado no recorte `[32:-32, 32:-32]`, comum aos pares
e distante das bordas perdidas. Exige-se erro menor que 15 níveis de intensidade
e, nos pares deslocados, menor que 25% do erro anterior ao alinhamento.
São tolerâncias de regressão deste cenário sintético, permitindo pequenas
diferenças de estimação e interpolação; não são métricas gerais de desempenho.
Também são verificados tamanho, tipo e preservação da imagem móvel.

Os casos de falha incluem imagem nula/vazia em cada entrada, falta de textura
em cada entrada, mínimo menor que quatro, exigência de correspondências acima
do limite de pontos do detector e formato de dois canais não suportado.

## Resultado e limites

Em 12/11/2026: **95 testes passaram**, com Python 3.15.0, NumPy 2.5.4,
OpenCV 4.14.0 e pytest 9.2.0.

A suíte inclui um teste da CLI `demonstracao`, executada em diretório temporário:
verifica a geração dos painéis, a redução do erro no par sintético, a mensagem
de falha sem textura registrada no JSON e a consistência do MAE com os PNGs salvos.
O guia `DEMONSTRACAO.md` descreve as comparações visuais já disponíveis.

Isso não valida alinhamento com rotação ou perspectiva, cenas reais, ausência
de sobreposição, qualidade da homografia em casos degenerados ou desempenho.
Também faltam testes dos subcomandos individuais da CLI, de parâmetros não finitos e de tipos de dados
incompatíveis. Os testes de cubic verificam identidade e cor constante, sem
comparação quantitativa em padrões variáveis. Não foram gerados slides
ou resultados sobre imagens reais nesta etapa.
