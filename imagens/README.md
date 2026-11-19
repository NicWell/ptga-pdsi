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

As mídias locais nessas pastas são ignoradas pelo Git. A coleção inicial contém amostras sintéticas geradas pelo próprio projeto.
