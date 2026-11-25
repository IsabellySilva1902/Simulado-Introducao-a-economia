"""Gera index.html (o simulado) a partir de data/<assunto>.json e tools/template.html.

Uso, na raiz do repositório:  python3 tools/build.py

Cada arquivo em data/ é um assunto:
  {"assunto", "category", "prefixo", "fonte", "questoes": [
     {"s": subtema, "d": "B|I|A", "q": enunciado, "a": [5 alternativas],
      "j": [5 justificativas], "c": índice da correta, "p": ponto-chave,
      "t": tabela opcional {"headers", "rows"}, "ficha": caderno de erros}
  ]}

O script converte para o formato do motor (o mesmo do vat2-simulados),
distribui a letra do gabarito entre A e E (só muda a ordem, nunca o texto)
e numera as questões. O motor ainda embaralha as alternativas a cada tentativa.
"""
import json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LETRAS = 'ABCDE'
DIF = {'B': 'Básica', 'I': 'Intermediária', 'A': 'Avançada'}
NOME = 'Introdução à Economia'
STORAGE = 'intro-economia'
# os arquivos "-b" (2º lote) vêm depois, para não mudar a letra das 50 primeiras
ORDEM = ['consumo', 'producao', 'custos', 'lucro', 'consumo-b', 'producao-b', 'custos-b', 'lucro-b']


def converter(q, codigo, d):
    c = q['c']
    def rotulo(k):
        if k == c:
            return 'CORRETA. '
        # em "marque a INCORRETA/ERRADA", a alternativa que não é resposta é uma frase verdadeira
        return 'Não é a resposta. ' if q['j'][k].startswith('Verdadeira') else 'Incorreta. '
    opts = [{'letter': LETRAS[k], 'text': q['a'][k].strip(), 'rationale': rotulo(k) + q['j'][k].strip()}
            for k in range(5)]
    saida = {
        'code': codigo, 'assunto': d['assunto'], 'category': d['category'],
        'subcategory': q['s'], 'difficulty': DIF[q['d']], 'origem': 'nova',
        'sourceLabel': d['fonte'], 'prompt': q['q'].strip(), 'options': opts,
        'correctLetter': LETRAS[c], 'clinicalPointers': q['p'], 'revisada': True,
    }
    if q.get('t'):
        saida['visual'] = {'type': 'table', 'headers': q['t']['headers'], 'rows': q['t']['rows']}
    if q.get('ficha'):
        f = dict(q['ficha'])
        f['topicos'] = [dict(t, sub=t.get('sub', [])) for t in f['topicos']]
        f.setdefault('fonte', d['fonte'])
        saida['ficha'] = f
    return saida


def main():
    banco = []
    for nome in ORDEM:
        d = json.load(open(os.path.join(RAIZ, 'data', nome + '.json'), encoding='utf-8'))
        for n, q in enumerate(d['questoes'], d.get('inicio', 1)):
            assert len(q['a']) == 5 and len(q['j']) == 5, f"{d['prefixo']}-{n:02d}: precisa de 5 alternativas"
            banco.append(converter(q, f"{d['prefixo']}-{n:02d}", d))
        print(f"{nome}.json: {len(d['questoes'])} questões ({d['category']})")

    # distribui o gabarito entre A-E: troca só a posição das alternativas
    for i, q in enumerate(banco):
        alvo = LETRAS[(i * 3 + 1) % 5]
        o = q['options']
        correta = o.pop(LETRAS.index(q['correctLetter']))
        o.insert(LETRAS.index(alvo), correta)
        for k, x in enumerate(o):
            x['letter'] = LETRAS[k]
        q['correctLetter'] = alvo

    for i, q in enumerate(banco, 1):
        q['id'] = i

    ordem = ['id', 'code', 'assunto', 'category', 'subcategory', 'difficulty', 'origem',
             'sourceLabel', 'prompt', 'visual', 'options', 'correctLetter', 'clinicalPointers',
             'ficha', 'revisada']
    banco = [{k: q[k] for k in ordem if k in q} for q in banco]
    json.dump(banco, open(os.path.join(RAIZ, 'data', 'questoes.json'), 'w', encoding='utf-8'),
              ensure_ascii=False, indent=1)

    tpl = open(os.path.join(RAIZ, 'tools', 'template.html'), encoding='utf-8').read()
    pagina = (tpl.replace('estilo ENAMED/residência', 'no estilo das provas da disciplina')
                 .replace('Estilo ENAMED / prova de residência', 'Microeconomia · consumo e firma')
                 .replace('SIMULADO DE FARMACOLOGIA CLÍNICA', 'SIMULADO DE ' + NOME.upper())
                 .replace('{{NOME}}', NOME).replace('{{STORAGE}}', STORAGE)
                 .replace('{{BANCO}}', json.dumps(banco, ensure_ascii=False, indent=1)))
    open(os.path.join(RAIZ, 'index.html'), 'w', encoding='utf-8').write(pagina)

    letras = {}
    for q in banco:
        letras[q['correctLetter']] = letras.get(q['correctLetter'], 0) + 1
    print(f"\nindex.html gerado: {len(banco)} questões, gabarito {dict(sorted(letras.items()))}")


if __name__ == '__main__':
    main()
