# Instruções para agentes de programação (Codex)

Leia primeiro `CONTEXTO_PROJETO.md` e `README.md` antes de alterar qualquer arquivo. Estes arquivos são documentação permanente de contexto e **devem permanecer versionados**.

## Missão
Implementar e documentar o projeto acadêmico **Transformações Geométricas e Alinhamento** para PDSI, usando Python e OpenCV. A entrega oficial inclui uma apresentação e um repositório; haverá acompanhamento e apresentação final, 10–15 min cada.

## Diretrizes
- Preserve os nomes dos membros da equipe e diferencie sempre **exigência do professor**, **sugestão** e **funcionalidade já implementada**.
- Mantenha o projeto simples: módulos Python reutilizáveis, testes e uma CLI funcionando. Não introduza React, FastAPI, banco de dados, Docker ou serviços externos sem solicitação expressa.
- Prefira `numpy` + `cv2`; explique a matriz e a interpolação usada em cada transformação.
- Em alinhamento, valide correspondências, estime transformação com RANSAC e lide com falhas sem resultados inventados.
- Faça testes com imagens sintéticas pequenas; imagens reais são materiais de teste opcionais; não comite datasets grandes ou arquivos sem licença clara.
- Sempre rode `python -m pytest -q` após mudanças relevantes e descreva quais testes executou.
- Não declare que há métricas, resultados, apresentação ou relatório prontos quando ainda não houver.
- Não modifique escopo/cronograma/datas sem explicitar a decisão.

## Áreas sugeridas
- `src/rotacao.py`, `src/translacao.py`, `src/espelhamento.py`, `src/redimensionamento.py`: geometria.
- `src/alinhamento.py`: registro ORB/RANSAC e tratamento de erros.
- `src/experimento_coco.py`: experimento local com as duas fotos descritas em `imagens/catalogo.json`; a suíte automatizada usa imagens sintéticas.
- `app.py`: CLI inicial; futura interface opcional.
- `tests/`: cobrir parâmetros, formatos, casos limite e falhas de alinhamento.

## Prioridade
Garantir protótipo demonstrável no acompanhamento em **19/11/2026** (data confirmada pelo integrante); depois qualidade experimental e documentação para entrega final. Os papéis da equipe são referências de organização, não restrições: o integrante autorizou executar o necessário em todas as áreas para viabilizar a entrega.

## Ponto de retomada

- O guia do código em `output/pdf/guia-do-codigo-pdsi.pdf` inclui o experimento COCO val2014. É material de apoio local, ignorado pelo Git. Preserve autoria, fonte e licença ao documentar as fotos e as versões transformadas.
- Diferencie os quatro alinhamentos com versões derivadas de cada foto do controle com cenas distintas. Consulte `imagens/README.md` para reproduzir e interpretar os resultados.
- A pedido do integrante, adie a validação com duas capturas sobrepostas da mesma cena para uma próxima sessão, quando ele retomar a etapa. Tempo, erro de reprojeção e ampliação da suíte são melhorias propostas. Registre como concluído apenas o que for executado e verificado.
