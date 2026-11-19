# Banco local de imagens

O catálogo registra as amostras iniciais e os pares de alinhamento. Os caminhos em `catalogo.json` são relativos a esta pasta. O catálogo serve como referência para os experimentos e os comandos continuam recebendo os caminhos dos arquivos.

## Gerar as amostras sintéticas

Na raiz do projeto, com o ambiente virtual ativado, execute:

```powershell
python app.py demonstracao --destino imagens/testes/sinteticas
```

O comando gera também os painéis e o resumo da demonstração no mesmo destino. Para reproduzir o caso de alinhamento catalogado:

```powershell
python app.py alinhamento --referencia imagens/testes/sinteticas/original.png --movel imagens/testes/sinteticas/movel.png --saida resultados/catalogo-alinhada.png
```

## Acrescentar fotografias

Guarde os originais em `imagens/originais/` e derivados de teste em `imagens/testes/`. Registre no catálogo o identificador, o caminho, a autoria, a fonte e a licença ou permissão de uso. Para um par de registro, fotografe a mesma cena com sobreposição e registre qual arquivo é a referência e qual é a imagem móvel.

As mídias locais nessas pastas são ignoradas pelo Git.

## Reproduzir o teste com o COCO val2014

Com os arquivos `000000019221.jpg` e `000000044652.jpg` em `imagens/originais/`, execute na raiz:

```powershell
python -m src.experimento_coco
```

Abra `resultados/coco/resumo.json` e os painéis nas subpastas de cada imagem. O experimento usa rotação de +15°, translação de (+40, -25) pixels, espelhamento horizontal e redução à metade das dimensões (arredondadas para baixo) com interpolação por área. Para cada original, o alinhamento usa duas versões derivadas da mesma foto, uma por rotação e outra por perspectiva. O JSON registra a matriz aplicada, o número de pixels avaliados e o erro absoluto médio (MAE) antes e depois. O MAE usa os canais BGR na área em comum estimada com a transformação conhecida, com erosão de dois pixels no contorno da máscara.

As duas fotos originais retratam cenas distintas. Elas também são cruzadas como controle de falha, no sentido de `000000044652.jpg` para `000000019221.jpg`. Os resultados cobrem essas amostras e os parâmetros escolhidos. Pares de duas capturas sobrepostas da mesma cena ainda não foram avaliados.

### Resultados registrados

| Amostra | Dimensões | MAE rotação (antes → depois) | MAE perspectiva (antes → depois) |
|---|---:|---:|---:|
| `000000019221.jpg` (brócolis) | 640 × 478 | 42,72 → 1,65 | 26,10 → 1,83 |
| `000000044652.jpg` (avião) | 640 × 427 | 24,83 → 1,05 | 21,75 → 4,69 |

Execução com OpenCV 4.14.0 e NumPy 2.5.4. O controle de cenas distintas foi
rejeitado com quatro correspondências após o filtro de razão, abaixo do mínimo
de dez. A rejeição ocorreu antes da estimação RANSAC.

### Créditos das fotografias

Os IDs e as licenças foram conferidos em `captions_val2014.json`, no pacote
[oficial de anotações COCO 2014](https://s3.amazonaws.com/images.cocodataset.org/annotations/annotations_trainval2014.zip),
e cruzados com os metadados públicos do Flickr.

| Arquivo local | Autoria e foto original | Licença |
|---|---|---|
| `000000019221.jpg` | [Krijn Schuurman](https://www.flickr.com/photos/krijn/6237638989/) | [CC BY-NC-SA 2.0](https://creativecommons.org/licenses/by-nc-sa/2.0/) |
| `000000044652.jpg` | [west.m](https://www.flickr.com/photos/westm/5977306745/) | [CC BY-NC 2.0](https://creativecommons.org/licenses/by-nc/2.0/) |

Ao usar as imagens em slides, inclua a autoria, o link da foto e a licença.
Identifique as versões transformadas e observe as condições da licença de cada foto.
