# Simulado de Introdução à Economia

Simulado interativo de Microeconomia com 50 questões comentadas de múltipla escolha (a–e), no estilo das provas da disciplina. Cada questão tem uma ficha de caderno de erros.

| Assunto | Questões |
|---|---|
| Teoria do consumo (cestas, restrição orçamentária, preferências, curvas de indiferença, TMS) | 18 |
| Teoria da produção (função de produção, curto e longo prazo, PT, Pme, Pmg, lei dos rendimentos, rendimentos de escala) | 17 |
| Teoria dos custos (CFT, CVT, custos médios, CMg, curto e longo prazo) | 10 |
| Maximização de lucros (LT, RT, RMg, condição RMg = CMg) | 5 |

Fontes: Vasconcellos, *Economia Micro e Macro* (caps. 5 a 7) e as provas antigas usadas como modelo de estilo.

## Atualizar

As questões ficam em `data/<assunto>.json`. Depois de editar, rode na raiz:

    python3 tools/build.py

Isso gera `index.html` e `data/questoes.json`.
