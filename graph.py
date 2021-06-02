import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt
import mplcyberpunk
import matplotlib
from numpy import arange, sin, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
matplotlib.use('TkAgg')



file = [{'id': 1, 'value': '1077', 'description': 'Saldo inicial', 'date': '29/03/20', 'parc': '1', 'type': 'Credit',
         'sub': 'None'},
        {'id': 2, 'value': '-40.25', 'description': 'Mercado', 'date': '29/03/20', 'parc': '1', 'type': 'Debit',
         'sub': [{'sValue': '11.98', 'sDesc': 'Pepsi 2L 2x'}, {'sValue': '3.78', 'sDesc': 'Agua 1.5L 2x'},
                 {'sValue': '4.7', 'sDesc': 'Cheetos Onda 2x'}, {'sValue': '5.78', 'sDesc': 'Fandangos presunto 2x'},
                 {'sValue': '4.7', 'sDesc': 'Cheetos lua 2x'}, {'sValue': '5.82', 'sDesc': 'Maça red 0.53 kg'},
                 {'sValue': '3.49', 'sDesc': 'BIS'}]},
        {'id': 3, 'value': '-29.65', 'description': 'mercado', 'date': '01/04/20', 'parc': '1', 'type': 'Debit',
         'sub': [{'sValue': '3.78', 'sDesc': 'Agua 1.5L 2x'}, {'sValue': '5.99', 'sDesc': 'Pepsi 2L'},
                 {'sValue': '14.9', 'sDesc': 'Azeite andorinha 500ml'}, {'sValue': '1.05', 'sDesc': 'alho 0.05kg'},
                 {'sValue': '2.35', 'sDesc': 'manjericao'}, {'sValue': '1.58', 'sDesc': 'ative plus 290ml 2x'}]},
        {'id': 4, 'value': '800', 'description': 'pensao', 'date': '31/03/20', 'parc': '1', 'type': 'Credit',
         'sub': 'None'},
        {'id': 5, 'value': '-67.6', 'description': 'mercado', 'date': '03/04/20', 'parc': '1', 'type': 'Debit',
         'sub': [{'sValue': '5.99', 'sDesc': 'Pepsi 2L'}, {'sValue': '6.99', 'sDesc': 'Coca 2L'},
                 {'sValue': '8.13', 'sDesc': 'Maça red 0.74kg'}, {'sValue': '6.38', 'sDesc': 'Leite 1L 2x'},
                 {'sValue': '11.99', 'sDesc': 'Texas burger'}, {'sValue': '2.35', 'sDesc': 'Cheetos Onda'},
                 {'sValue': '19.33', 'sDesc': 'patinho moido 0.614kg'}, {'sValue': '2.35', 'sDesc': 'Cheetos Lus'},
                 {'sValue': '4.09', 'sDesc': 'peito peru 0.1kg'}]},
        {'id': 6, 'value': '-15.25', 'description': 'Mercado', 'date': '05/04/20', 'type': 'Debit',
         'sub': [{'sValue': '3.49', 'sDesc': 'Pepsi 1.5L'}, {'sValue': '4.74', 'sDesc': 'Ative plus 290ML 6x'},
                 {'sValue': '0.92', 'sDesc': 'limão tahiti 0.23kg'},
                 {'sValue': '6.1', 'sDesc': 'queijo muçarela imp 0.232kg'}]},
        {'id': 7, 'value': '-920.0', 'description': 'aluguel abril', 'date': '06/04/20', 'type': 'Debit',
         'sub': 'None'},
        {'id': 8, 'value': '-50.81', 'description': 'Mercado', 'date': '07/04/20', 'type': 'Debit',
         'sub': [{'sValue': '4.19', 'sDesc': 'Pepsi 1.5L'}, {'sValue': '6.99', 'sDesc': 'Coca 2L'},
                 {'sValue': '11.29', 'sDesc': 'Sabão em pó Tixan 2k'}, {'sValue': '4.94', 'sDesc': 'Banana 0.99kg'},
                 {'sValue': '4.79', 'sDesc': 'Pão de forma Wickbold'}, {'sValue': '4.15', 'sDesc': 'Farofa Yoki'},
                 {'sValue': '2.35', 'sDesc': 'Cheetos onda'}, {'sValue': '4.99', 'sDesc': 'Cebolitos'},
                 {'sValue': '2.35', 'sDesc': 'Cheetos lua'}, {'sValue': '4.77', 'sDesc': 'miojo'}]},
        {'id': 9, 'value': '-25.45', 'description': 'Mercado', 'date': '09/04/20', 'type': 'Debit',
         'sub': [{'sValue': '11.98', 'sDesc': 'Pepsi 2L 2x'}, {'sValue': '2.25', 'sDesc': 'Ative plus 3x'},
                 {'sValue': '4.25', 'sDesc': 'Piraque coco'}, {'sValue': '2.27', 'sDesc': 'Cebola 0.455kg'},
                 {'sValue': '4.7', 'sDesc': 'Cheetos Lua 2x'}]},
        {'id': 10, 'value': '-93.43', 'description': 'Mercado', 'date': '12/04/20', 'type': 'Debit',
         'sub': [{'sValue': '3.78', 'sDesc': 'agua petropolis 2x'}, {'sValue': '11.98', 'sDesc': 'pepsi 2l 2x'},
                 {'sValue': '14.39', 'sDesc': 'ovos caipira 10u'}, {'sValue': '7.12', 'sDesc': 'peito peru 0.238kg'},
                 {'sValue': '19.37', 'sDesc': 'patinho bovino 0.72kg'},
                 {'sValue': '7.99', 'sDesc': 'requeijão danubio trad'},
                 {'sValue': '6.38', 'sDesc': 'leite glória 1l 2x'}, {'sValue': '4.9', 'sDesc': 'molho tomate heinz'},
                 {'sValue': '4.14', 'sDesc': 'maça gala 0.46kg'}, {'sValue': '8.39', 'sDesc': 'queijo ralado vigor'},
                 {'sValue': '4.99', 'sDesc': 'macarrao grano duro knorr'}]},
        {'id': 11, 'value': '-52.16', 'description': 'Mercado', 'date': '15/04/20', 'type': 'Debit',
         'sub': [{'sValue': '5.99', 'sDesc': 'Pepsi 2L'}, {'sValue': '6.99', 'sDesc': 'Coca-Cola 2L'},
                 {'sValue': '33.23', 'sDesc': 'Patinho bife 1.01kg'}, {'sValue': '2.76', 'sDesc': 'Alho 0.12kg'},
                 {'sValue': '3.19', 'sDesc': 'Arroz qualitá 1kg'}]},
        {'id': 12, 'value': '820', 'description': 'Bolsa estágio março', 'date': '15/04/20', 'type': 'Credit',
         'sub': 'None'},
        {'id': 13, 'value': '550', 'description': 'Vô Juca', 'date': '15/04/20', 'type': 'Credit', 'sub': 'None'},
        {'id': 14, 'value': '-37.87', 'description': 'Mercado', 'date': '17/04/20', 'type': 'Debit',
         'sub': [{'sValue': '6.99', 'sDesc': 'Pão de forma Panco'}, {'sValue': '1.89', 'sDesc': 'Aguá Crystal 1.5L'},
                 {'sValue': '5.99', 'sDesc': 'Pepsi 2L'}, {'sValue': '5.92', 'sDesc': 'Copo Summer 390ml'},
                 {'sValue': '6.96', 'sDesc': 'Queijo muçarela 0.364kg'}, {'sValue': '3.98', 'sDesc': 'Cheetos Lua 51g'},
                 {'sValue': '6.14', 'sDesc': 'Peito de Peru 0.162kg'}]},
        {'id': 15, 'value': '-46.68', 'description': 'Mercado', 'date': '19/04/20', 'type': 'Debit',
         'sub': [{'sValue': '11.98', 'sDesc': 'Pepsi 2L'}, {'sValue': '14.99', 'sDesc': 'Hamburguer Seara 672G'},
                 {'sValue': '5.52', 'sDesc': 'Banana 0.79kg'}, {'sValue': '3.49', 'sDesc': 'Leite Elege Semi'},
                 {'sValue': '4.77', 'sDesc': 'Miojo 3x'}, {'sValue': '3.98', 'sDesc': 'Cheetos Lua 2x'},
                 {'sValue': '1.95', 'sDesc': 'Cebola 0.325kg'}]},
        {'id': 16, 'value': '-69.79', 'description': 'Mercado', 'date': '22/04/20', 'type': 'Debit',
         'sub': [{'sValue': '7.98', 'sDesc': 'Pepsi 1.5L 2x'}, {'sValue': '4.15', 'sDesc': 'Molho de tomate heinz'},
                 {'sValue': '24.4', 'sDesc': 'Alcatra com maminha 0.98kg'},
                 {'sValue': '11.39', 'sDesc': 'Ovo banco 10x'}, {'sValue': '2.89', 'sDesc': 'Coca 350ml'},
                 {'sValue': '7.99', 'sDesc': 'Queijo ralado vigor'},
                 {'sValue': '10.99', 'sDesc': 'Requeijão Danubio'}]},
        {'id': 17, 'value': '-69.43', 'description': 'Mercado', 'date': '25/04/20', 'type': 'Debit',
         'sub': [{'sValue': '7.58', 'sDesc': 'Pepsi 1.5L 2x'}, {'sValue': '1.89', 'sDesc': 'Água Crystal 1.5L'},
                 {'sValue': '4.93', 'sDesc': 'Banana prata 0.76kg'}, {'sValue': '6.99', 'sDesc': 'pão de forma Panco'},
                 {'sValue': '6.36', 'sDesc': 'Miojo Carne 4x'}, {'sValue': '20.18', 'sDesc': 'Alcatra 0.93kg'},
                 {'sValue': '7.81', 'sDesc': 'Queijo Muçarela Nacional 0.296'},
                 {'sValue': '7.31', 'sDesc': 'Peito peru Sadia 0.174kg'},
                 {'sValue': '6.38', 'sDesc': 'Leite semi Italac 1L 2x'}]},
        {'id': 18, 'value': '-23.59', 'description': 'Mercado', 'date': '28/04/20', 'type': 'Debit',
         'sub': [{'sValue': '7.98', 'sDesc': 'Pepsi 1.5L 2x'}, {'sValue': '3.98', 'sDesc': 'Água Minalba 1.5L 2x'},
                 {'sValue': '4.29', 'sDesc': 'Catchup Franz 400g'}, {'sValue': '2.64', 'sDesc': 'Cebola 0.44kg'},
                 {'sValue': '4.7', 'sDesc': 'Cheetos Lua 2x'}]},
        {'id': 19, 'value': '-58.09', 'description': 'Mercado', 'date': '01/05/20', 'type': 'Debit',
         'sub': [{'sValue': '3.78', 'sDesc': 'Água crystal 2x'}, {'sValue': '6.98', 'sDesc': 'Pepsi 1.5L 2x'},
                 {'sValue': '4.58', 'sDesc': 'Cheetos Lua 2x'}, {'sValue': '25.93', 'sDesc': 'Contra file 0.788kg'},
                 {'sValue': '3.59', 'sDesc': 'leite quata 1L'}, {'sValue': '4.59', 'sDesc': 'Arroz tio joão 1kg'},
                 {'sValue': '4.75', 'sDesc': 'Banana prata 0.68kg'},
                 {'sValue': '3.89', 'sDesc': 'Margarina Claybom 500ml'}]},
        {'id': 20, 'value': '820', 'description': 'Bolsa Estágio', 'date': '04/05/20', 'type': 'Credit', 'sub': 'None'},
        {'id': 21, 'value': '800', 'description': 'Pensão abril', 'date': '04/05/20', 'type': 'Credit', 'sub': 'None'},
        {'id': 22, 'value': '-920.0', 'description': 'Aluguel', 'date': '06/05/20', 'type': 'Debit', 'sub': 'None'},
        {'id': 23, 'value': '-58.87', 'description': 'Mercado', 'date': '06/05/20', 'type': 'Debit',
         'sub': [{'sValue': '6.98', 'sDesc': 'Pepsi 1.5L 2x'}, {'sValue': '8.99', 'sDesc': 'Hamburguer qualitá'},
                 {'sValue': '5.07', 'sDesc': 'Toddynho 200ml 3x'}, {'sValue': '5.89', 'sDesc': 'Ovos Vermelho 6x'},
                 {'sValue': '20.1', 'sDesc': 'Patinho resfriado 0.576kg'},
                 {'sValue': '5.7', 'sDesc': 'Queijo Muçarela 0.154'},
                 {'sValue': '6.14', 'sDesc': 'Peito Peru 0.176kg'}]},
        {'id': 24, 'value': '-103.12', 'description': 'Mercado', 'date': '10/05/20', 'type': 'Debit',
         'sub': [{'sValue': '6.98', 'sDesc': 'Pepsi 1.5L 2x'}, {'sValue': '3.78', 'sDesc': 'Água Petropolis 1.5L 2x'},
                 {'sValue': '3.59', 'sDesc': 'Leite integral Quata 1L'},
                 {'sValue': '4.35', 'sDesc': 'Pão de forma seven boys'}, {'sValue': '4.77', 'sDesc': 'Miojo 3x'},
                 {'sValue': '8.99', 'sDesc': 'Lasanha bolonhesa perdigão'},
                 {'sValue': '7.99', 'sDesc': 'Requeijão Danubio'}, {'sValue': '3.85', 'sDesc': 'Biscoito Piraquê'},
                 {'sValue': '14.38', 'sDesc': 'Patinho 0.412kg'}, {'sValue': '11.03', 'sDesc': 'Patinho 0.316kg'},
                 {'sValue': '27.99', 'sDesc': 'Chinelo Havaianas'}, {'sValue': '2.62', 'sDesc': 'Cebola 0.375kg'},
                 {'sValue': '2.80', 'sDesc': 'Alho 0.1kg'}]},
        {'id': 25, 'value': '-20.55', 'description': 'Luftal 40mg', 'date': '13/05/20', 'type': 'Debit', 'sub': 'None'},
        {'id': 26, 'value': '-38.59', 'description': 'Mercado', 'date': '13/05/20', 'type': 'Debit',
         'sub': [{'sValue': '7.98', 'sDesc': 'Pepsi 1.5L 2x'}, {'sValue': '5.99', 'sDesc': 'Farofa de milho Yoki 500g'},
                 {'sValue': '7.99', 'sDesc': 'Manteiga Elege 200g'}, {'sValue': '3.95', 'sDesc': 'Biscoito Piraque'},
                 {'sValue': '4.29', 'sDesc': 'Pimenta do Reino Kit'},
                 {'sValue': '8.39', 'sDesc': 'Queijo Ralado Vigor'}]},
        {'id': 27, 'value': '-88.53', 'description': 'Mercado', 'date': '15/05/20', 'type': 'Debit',
         'sub': [{'sValue': '3.78', 'sDesc': 'Agua Crystal 1.5L 2x'}, {'sValue': '2.59', 'sDesc': 'Cheetos Lua'},
                 {'sValue': '3.95', 'sDesc': 'Biscoito Piraque'}, {'sValue': '7.92', 'sDesc': 'Peito de peru 0.198'},
                 {'sValue': '3.63', 'sDesc': 'Queijo Muçarela 0.098kg'},
                 {'sValue': '7.99', 'sDesc': 'Pão de queijo 400g'}, {'sValue': '35.11', 'sDesc': 'Patinho 1.006'},
                 {'sValue': '9.19', 'sDesc': 'Ovos Brancos'}, {'sValue': '6.59', 'sDesc': 'Achocolatado'},
                 {'sValue': '7.78', 'sDesc': 'Leite Elege 1L 2x'}]}]

data = {}
dates_list = []
values_list = []


def f_graph(username):
    # plt.close()
    for d in file:
        if d['date'] in data:
            n_value = float(d['value']) + float(data.get(d['date']))
            data.update({d['date']: str(n_value)})
        else:
            data.update({d['date']: d['value']})
    ordered_data = sorted(data.items(), key=lambda k: dt.datetime.strptime(k[0], '%d/%m/%y'),
                          reverse=False)
    for d, v in ordered_data:
        values_list.append(float(v))
        dates_list.append(d)
    series = pd.Series(values_list, dtype='float64')
    cumulative_sum = series.cumsum()
    serialized_date = [dt.datetime.strptime(d, '%d/%m/%y').date() for d in dates_list]
    plt.style.use("cyberpunk")
    plt.plot(serialized_date, cumulative_sum, 'm', marker='o')
    plt.xticks(rotation=20)
    plt.subplots_adjust(right=0.95, top=0.93, bottom=0.15)
    plt.title('Saldo ao longo do tempo.')
    fig = plt.gcf()
    manager = plt.get_current_fig_manager()
    fig.canvas.set_window_title('Gráfico do saldo de ' + username)
    # manager.window.wm_iconbitmap(resource_path('icon.ico'))
    # manager.window.SetPosition()
    plt.xlabel('Data')
    plt.ylabel('Saldo')
    mplcyberpunk.add_glow_effects()
    plt.show()

