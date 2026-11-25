# Simulado de Introdução à Economia

Simulado interativo de Microeconomia com 100 questões comentadas de múltipla escolha (a–e), no estilo das provas da disciplina. Cada questão tem uma ficha de caderno de erros.

| Assunto | Questões |
|---|---|
| Teoria do consumo (cestas, restrição orçamentária, preferências, curvas de indiferença, TMS) | 32 |
| Teoria da produção (função de produção, curto e longo prazo, PT, Pme, Pmg, lei dos rendimentos, rendimentos de escala) | 31 |
| Teoria dos custos (CFT, CVT, custos médios, CMg, curto e longo prazo) | 24 |
| Maximização de lucros (LT, RT, RMg, condição RMg = CMg) | 13 |

Fontes: Vasconcellos, *Economia Micro e Macro* (caps. 5 a 7) e as provas antigas usadas como modelo de estilo.

## Atualizar

As questões ficam em `data/<assunto>.json` (1º lote) e `data/<assunto>-b.json` (2º lote). Todas foram conferidas no NotebookLM. Depois de editar, rode na raiz:

    python3 tools/build.py

Isso gera `index.html` e `data/questoes.json`.
