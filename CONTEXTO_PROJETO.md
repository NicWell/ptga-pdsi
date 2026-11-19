# Contexto consolidado — Projeto de PDSI

> Documento preparado para passar o histórico e decisões da equipe ao Codex. Atualizado em **12/11/2026**. Distingue fatos documentados, informações informadas pela equipe e recomendações do assistente. Não substitui os PDFs do professor.

## 1. Identificação

- Disciplina: **Processamento Digital de Sinais e Imagens (PDSI)**.
- Tema escolhido: **Projeto 5 — Transformações Geométricas e Alinhamento**.
- Equipe (3 pessoas): **Vitória Regina dos Santos Melo**, **Antônio Elvis Pinheiro Nascimento da Silva** e **Wellington Nicacio Gama Canuto**.
- Situação: o repositório GitHub já foi criado pelo integrante; a estrutura inicial está sendo anexada. O endereço do repositório não foi informado nesta conversa.

## 2. Orientações do professor — fonte primária

Arquivo enviado: **Projetos de PDSI.docx.pdf**, 5 páginas. No tópico Projeto 5 (final da p. 2 / início da p. 3):

- Descrição: “Aplicar transformações como rotação, translação, espelhamento, redimensionamento e alinhamento entre imagens.”
- Objetivo: “Explorar transformações espaciais e registro de imagens.”
- Tecnologias: **Python, OpenCV**.
- Dataset: **COCO dataset** (sugerido, não necessariamente obrigatório).

Regras gerais no início do documento:

- Grupos de **2 a 4 pessoas**.
- **Apresentação de acompanhamento**: 10 a 15 minutos.
- **Apresentação final**: 10 a 15 minutos.
- **Entregáveis**: apresentação e repositório no GitHub ou outro repositório.
- O documento não especifica datas exatas, quantidade mínima de imagens, interface gráfica, relatório obrigatório ou métricas mandatórias.

## 3. Comunicação posterior do professor

Mensagem compartilhada pelo integrante:

> “Bom dia, pessoal! Espero que todos estejam bem. Para os que tiverem interesse, em anexo segue um relatório (**HDR_Relatorio.pdf**) de um dos projetos feitos em 2025.2. Ele contêm a descrição do problema, link para o github e também principais resultados. Lembrando que essa semana e a próxima são de acompanhamento, conforme link do doc em anexo. Quaisquer dúvidas me encontro à disposição. Até mais.”

O integrante informou em **12/11/2026** que **houve a primeira parte das apresentações hoje**, mas seu grupo não foi selecionado; **o grupo participará do acompanhamento na semana seguinte**. Inicialmente a data exata não estava confirmada. Posteriormente, o integrante confirmou **19/11/2026** como o dia do acompanhamento; o horário ainda não foi informado.

## 4. Relatório disponibilizado como exemplo (não é rubric/obrigação)

Arquivo: **HDR_Relatorio.pdf** (25 páginas), exemplo de 2025.2, elaborado por outro grupo do IFAL Campus Arapiraca, curso Sistemas de Informação. Tema diferente: ferramenta **HDR Converter** para conversão de imagens HDR/EXR em RGBM para aplicações com texturas em jogos.

Organização do exemplo:

1. Descrição do problema, soluções existentes e objetivos;
2. Tecnologias e ferramentas utilizadas;
3. Descrição da solução, tentativas, algoritmos, aplicação, resultados, usos práticos, teste de desempenho e considerações finais;
4. Referências.

O exemplo usa Python, OpenCV, NumPy, GUI PySide6, GitHub e compara visualmente resultados. Na seção de desempenho mede tempos em **cinco execuções** por configuração e apresenta médias. Repositório informado no relatório: https://github.com/Maheshivara/hdr-converter.

**Atenção:** não foi solicitado formalmente reproduzir interface PySide6, aplicativo `.exe`, relatório de 25 páginas ou testes idênticos. O arquivo orienta o nível de documentação e apresentação que pode ser útil.

## 5. Proposta da equipe / sugestões discutidas (não imposições do professor)

Desenvolver aplicação Python para:

1. **Rotação**: grau configurável (matrizes, centro, bordas/interpolação).
2. **Translação**: deslocamentos horizontais e verticais em pixels.
3. **Espelhamento**: horizontal, vertical, ambos.
4. **Redimensionamento**: escala/dimensões, comparação entre nearest/linear/cubic/area.
5. **Alinhamento de duas imagens**: detectar pontos ORB, associar descritores, estimar homografia com RANSAC e aplicar `warpPerspective` (alternativamente, modelo afim quando adequado).
6. **Visualização e salvamento** das imagens; eventualmente comparação antes/depois.

Arquitetura: módulos em `src/`, uma CLI simples `app.py` para primeira entrega, testes em `tests/`; possível UI **Streamlit** ou **PySide6** somente se sobrarem tempo e interesse. **Não foi decidida uma interface obrigatória.**

Cuidados técnicos:
- COCO é sugerido para imagens, mas não necessariamente fornece pares de registro de uma mesma cena. Para validar registro, gerar pares sintéticos com transformações conhecidas a partir de imagens escolhidas, e eventualmente captar fotografias reais sobrepostas.
- ORB/RANSAC não garante alinhamento em cenas sem textura, com poucos pontos ou sem sobreposição.
- Avaliar com evidências visuais, parâmetros de transformação conhecidos, erro de reprojeção e, quando fizer sentido, RMSE/SSIM em regiões comuns (excluindo bordas inválidas). Métricas são sugestões.
- Documentar erros e limitações, não apenas exemplos favoráveis.

## 6. Repartição de responsabilidades aceita pela equipe

O integrante confirmou em **12/11/2026** que as responsabilidades abaixo foram aceitas pelos integrantes. Trata-se de uma decisão da equipe.

- **Vitória:** teoria, rotação, translação e espelhamento.
- **Antônio Elvis:** redimensionamento, interpolação, comparações/testes.
- **Wellington:** integração, GitHub, alinhamento automático.
- Todos: discussão de alinhamento, testes e apresentações.

O integrante esclareceu que essa divisão não limita a execução: o necessário
para a entrega pode ser desenvolvido em qualquer área, inclusive pelo Codex,
independentemente do responsável de referência. A prioridade é o acompanhamento
em **19/11/2026**.

O assistente propôs divisão das falas em aproximadamente quatro minutos para cada pessoa; **isso não foi confirmado como acordo da equipe**.

## 7. Plano sugerido para acompanhamento

Apresentar de 10 a 15 minutos:

- Problema e objetivos.
- Fundamentação breve das matrizes de transformação e de registro.
- Demonstração real das quatro transformações, preferencialmente já funcionais.
- Se possível, protótipo e limitações iniciais de alinhamento.
- Próximas etapas e progresso no GitHub.

O acompanhamento está confirmado pelo integrante para **19/11/2026**. Um roteiro proposto foi: organização e preparação (12–13/11), transformações básicas (14–15/11), alinhamento (16/11), evidências (17/11) e ensaio/slides (18/11). Essas etapas intermediárias são **datas de planejamento**, não prazos anunciados pelo professor.

## 8. Etapas após acompanhamento

- Validar algoritmos e parâmetros sobre imagens variadas.
- Medir desempenho e qualidade de registro com protocolo reproduzível.
- Produzir comparações com imagem original e transformada.
- Escrever uma descrição formal do problema, metodologia, implementação, resultados e conclusões (inspirada no HDR, se for útil ou exigido futuramente).
- Preparar apresentação final (10–15 min) e manter o repositório documentado.

## 9. Estado REAL do código no pacote inicial

- Existem módulos Python de rotação, translação, espelhamento e redimensionamento, CLI, testes mínimos e um **protótipo** ORB/RANSAC para alinhamento.
- Não existem ainda dataset COCO baixado, relatório formal, slides, resultados de experimentos com imagens reais, interface GUI nem avaliação de desempenho sistemática.
- Verificar localmente `python -m pytest -q` antes de apresentar a implementação como validada; executar demonstrações com imagens representativas.

## 10. Próxima tarefa sugerida para o Codex

> Leia `AGENTS.md`, `CONTEXTO_PROJETO.md` e `README.md`. Primeiro, confira os módulos e execute os testes. Em seguida, implemente uma rotina para gerar comparações visuais original/transformada; acrescente testes com transformações sintéticas conhecidas e documentação simples da metodologia. Preserve os requisitos do professor e não crie dependências de frontend/backend sem necessidade.

## 11. Progresso após o pacote inicial

- Ampliada a suíte de testes sintéticos de geometria e alinhamento por translação.
- Implementado `python app.py demonstracao`: gera imagens sintéticas, comparações
  das quatro operações, exemplo de alinhamento e registro de falha sem textura.
- A demonstração salva medições do par sintético em `resumo.json`, sem generalizar
  os resultados para cenas reais. Consulte `docs/DEMONSTRACAO.md`.
- Permanecem pendentes slides, ensaio, validação com imagens reais e avaliação
  experimental mais ampla; não há mudança nas exigências do professor.

## 12. Ponto de parada e resumo para a equipe — 12/11/2026

**O que temos:** CLI com as quatro transformações e protótipo ORB/RANSAC,
95 testes passando e uma demonstração sintética reproduzível. Nenhuma tecnologia
de interface ou serviço externo foi adicionada. As responsabilidades aceitas
continuam como referência, com colaboração em todas as áreas autorizada.
O acompanhamento foi confirmado para **19/11/2026**, sem horário informado.

**Verificação realizada:** `python -m pytest -q` pela `.venv` — 95 testes
passaram. `git diff --check` não apontou erros de espaços. O teste novo da CLI
executa a demonstração em diretório temporário, verifica os painéis e recalcula
o erro a partir dos PNGs salvos. Foram inspecionados visualmente os painéis de
rotação, alinhamento e detalhes de interpolação.

**Resultados locais:** `resultados/demonstracao/` contém 21 PNGs e `resumo.json`.
Inclui original, saídas individuais, comparações, detalhe de interpolação,
referência/móvel/alinhada e imagem sem textura. No par sintético de deslocamento
+12/-8 pixels, o MAE caiu de aproximadamente 40,39 para 1,97 na região comum.
Esse resultado é apenas desse cenário; não é uma avaliação em imagens reais.

**Como conferir:** na raiz, execute
`.\.venv\Scripts\python.exe app.py demonstracao` e abra os arquivos
`comparacao_*.png` em `resultados/demonstracao/`. Para repetir a verificação:
`.\.venv\Scripts\python.exe -m pytest -q`.
O guia completo está em `docs/DEMONSTRACAO.md`, e a metodologia dos testes
em `docs/TESTES_SINTETICOS.md`.

**Compartilhamento:** código e documentação devem ser versionados; as imagens
geradas estão ignoradas pelo Git. Colegas podem reproduzi-las com o comando
acima após instalar `requirements.txt`. A `.venv` também não é versionada.
O Codex não fez commit ou push; no encerramento desta sessão ainda há alterações
locais e arquivos novos da demonstração aguardando versionamento pelo integrante.

**Próxima retomada:** escolher imagens próprias ou com licença documentada,
validar exemplos reais e preparar slides/ensaio de 10–15 minutos. Também faltam
testes de registro com rotação/perspectiva, validação de homografias degeneradas
e parâmetros não finitos. A demonstração sintética está disponível; a apresentação
e a validação experimental ampla ainda não estão concluídas.

O integrante solicitou parar o desenvolvimento neste ponto; esta atualização
é apenas documental para facilitar o compartilhamento e a retomada.
