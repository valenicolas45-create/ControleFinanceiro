"""Projeto 05: receitas, despesas e agregacoes com valores em centavos."""
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from datetime import datetime, timezone
from conexao import banco
import csv


lancamentos = banco['lancamentos_p05']

def centavos(texto):
    try:
        valor = Decimal(texto.replace(',', '.'))
        if not valor.is_finite() or valor <= 0:
            raise ValueError
        return int((valor * 100).quantize(Decimal('1'), rounding=ROUND_HALF_UP))
    except (InvalidOperation, ValueError):
        return None

while True:
    print('\n[1] Registrar [2] Extrato [3] Resumo por categoria')
    print('[4] Filtrar por mês [5] Excluir lançamento [6] Gerar relatório CSV [0] Sair')
    op = input('Opção: ').strip()
    if op == '1':
        tipo = input('Tipo (receita/despesa): ').strip().lower()
        categoria = input('Categoria: ').strip()
        valor = centavos(input('Valor (R$): ').strip())
        if tipo not in ('receita', 'despesa') or not categoria or valor is None:
            print('Dados inválidos.'); continue
        lancamentos.insert_one({'tipo': tipo, 'categoria': categoria,
                                'valor_centavos': valor,
                                'criado_em': datetime.now(timezone.utc)})
        print('Lançamento registrado.')
    elif op == '2':
        for item in lancamentos.find().sort('criado_em', -1).limit(30):
            print(f"{item['tipo']} | {item['categoria']} | R$ {item['valor_centavos']/100:.2f}")
    elif op == '3':
        pipeline = [
            {'$group': {'_id': {'tipo': '$tipo', 'categoria': '$categoria'},
                        'total': {'$sum': '$valor_centavos'}}},
            {'$sort': {'_id.tipo': 1, '_id.categoria': 1}}
        ]
        receitas = despesas = 0
        for item in lancamentos.aggregate(pipeline):
            tipo, categoria = item['_id']['tipo'], item['_id']['categoria']
            total = item['total']
            print(f'{tipo} / {categoria}: R$ {total/100:.2f}')
            if tipo == 'receita': receitas += total
            else: despesas += total
        print(f'SALDO: R$ {(receitas - despesas)/100:.2f}')
    elif op == '4':
        periodo = input('Informe o mês e o ano (MM/AAAA): ').strip()
        try:
            mes, ano = periodo.split('/')
            mes = int(mes)
            ano = int(ano)
            if mes < 1 or mes > 12:
                raise ValueError
            inicio = datetime(ano, mes, 1, tzinfo=timezone.utc)
            if mes == 12:
                fim = datetime(ano + 1, 1, 1, tzinfo=timezone.utc)
            else:
                fim = datetime(ano, mes + 1, 1, tzinfo=timezone.utc)
        except ValueError:
            print('Data inválida. Utilize MM/AAAA.')
            continue
        filtro = {
            'criado_em': {
                '$gte': inicio,
                '$lt': fim
            }
        }
        resultados = list(
            lancamentos.find(filtro).sort('criado_em', -1)
        )
        if resultados:
            print(f'\nLançamentos de {mes:02d}/{ano}:\n')
            for item in resultados:
                print(
                    f"{item['tipo']} | {item['categoria']} | R$ {item['valor_centavos']/100:.2f}")
        else:
            print('Nenhum lançamento encontrado nesse período.')
    elif op == '5':
        resultados = list(lancamentos.find().sort('criado_em', -1))

        if resultados:
            for i, item in enumerate(resultados):
                print(f"[{i + 1}] {item['tipo']} | "
                      f"{item['categoria']} | "
                      f"R$ {item['valor_centavos']/100:.2f}")

            escolha = input('Digite o número do lançamento que deseja excluir: ').strip()

            if escolha.isdigit() and 1 <= int(escolha) <= len(resultados):
                posicao = int(escolha) - 1

                confirmar = input('Confirma a exclusão? (s/n): ').strip().lower()

                if confirmar == 's':
                    lancamentos.delete_one({'_id': resultados[posicao]['_id']})
                    print('Lançamento excluído com sucesso!')
                else:
                    print('Exclusão cancelada.')
            else:
                print('Opção inválida.')
    elif op == '6':
        resultados = lancamentos.find().sort('criado_em', -1)

        with open('relatorio_financeiro.csv', 'w',
                  newline='', encoding='utf-8-sig') as arquivo:

            escritor = csv.writer(arquivo, delimiter=';')

            escritor.writerow(['Tipo', 'Categoria', 'Valor (R$)', 'Data'])

            for item in resultados:
                escritor.writerow([
                    item['tipo'],
                    item['categoria'],
                    f"{item['valor_centavos']/100:.2f}".replace('.', ','),
                    item['criado_em'].strftime('%d/%m/%Y %H:%M:%S')
                ])

        print('Relatório CSV gerado com sucesso!')
    elif op == '0':
        break
    else:
        print('Opção inválida.')