from fakebullhouse.classes import Produto


cardapio = [ Produto(1, 'NELORE', 24.99,'Servido no delicioso pao de brioche com bife de 180grs assado na brasa com queijo prato, ovo, salada e dois molhos de sua preferencia, \ntem tudo que um tradicional hamburguer artesanal pode oferecer!!'),
             Produto(2, 'JAVALI', 29.99,'Delicioso bife 180grs de carne de costelinha suina asssado na brasa, com muito queijo canastra e bacon artesanal Bull, servido no Pão de gergelin \nacompanhado de ovo, salada e dois molho de sua preferencia!'),
             Produto(3, 'ANGUS', 34.99,'O nosso delicioso angus, suculento do inicio ao fim servido no pao de brioche bread maker com bife 100% carne de angus de 200 gramas \nacompanhando de muito queijo canastra, salada e dois molhos de sua preferencia!!'),
             Produto(4, 'ZEBU', 29.99,'Pao australiano acompanhado de bife de 180grs assado na brasa com queijo cheddar, bacon artesanal Bull ,ovo salada e dois molhos de sua preferencia'),
             Produto(5, 'GUZERÁ', 31.99,'Bife de 180grs assado na brasa queijo cheddar, bacon artesanal Bull, aneis de ceboola empanada, ovo salada e dois molhos de sua preferencia \nservido no pão australiano criando uma combinaçao perfeira!'),
             Produto(6, 'MINOTAURO', 41.99,'O nosso famoso Minotauro e grande no tamanho e gigante no sabor, feito com dois bifes de 180grs assado na brasa com duplo queijo cheddar duplo bacon artesanal \nBull servido no pao de gergelim com salada, ovo e dois molhos opcionais é perfeito para quem esta com fome de verdade!'),
             Produto(7, 'BEZERRO', 20.99,'Servido no pão de brioche com bife de 100 grs assado na brasa acompanhado de queijo prato, ovo, salada e dois molhos opcionais (kids)'),
             Produto(8, 'COCOTA', 29.99,'Pão de brioche, bife de 180grs de frango assado na brasa com bacon artesanal bull queijo cheddar salada, ovo \ndois molhos opcionais, voce vai amar esse gostinho de frango com bacon.'),
             Produto(9, 'CARACU', 31.99,'Feito com bife de 180grs assado na brasa com queijo cheddar, bacon artesanal Bull, ovo , cebola caramelizada \ne salada servido no pão de brioche uma combinaçao perfeita do sabor agridoce com churrasco.'),
             Produto(10, 'HOLANDÊS', 45.99,'Nosso monstro è feito com dois bifes de 180grs assados na brasa com duplo queijo cheddar, dublo bacon artesanal Bull, duplo ovo, \nsalaminho italiano cebola caramelizada servido no delicioso pao de gergelin e dois molhos de sua escolha,esse é gigante no tamanho e no sabor!'),
]

cardapio_refrigerante=[ Produto(11,'COCA COLA 2 LITROS',13.00,''),
                       Produto(12,'GUARANÁ ANTÁRTICA 2 LITROS',13.00,''),
                       Produto(13,'COCA COLA 1 LITROS',9.00,''),
                       Produto(14,'GUARANÁ ANTÁRTICA 1 LITROS',9.00,'')
]

cardapio_pocoes = [ Produto(15,'PORÇÕES BATATA FRITA COMPLETA',29.99,'DELICIOSA BATATA FRITA A PALITO ACOMPANHADA DE QUEIJO E BACOM'),
                    Produto(16,'BATATA INDIVIDUAL',10.00,''),
                    Produto(17,'PORÇÕES FRITAS SIMPLES',24.99,''),
                    ]



def limpar():
    print('\n' * 10)


def pausa():
    while True:
        opcao = input('\nENTER para continuar | 0 para escolher novamente: ')
        if opcao == '':
            return True
        elif opcao == '0':
            return False
        else:
            print('Opção inválida!')


def menu():
    print('1- HAMBÚRGUER')
    print('2- PORÇÕES')
    print('3- REFRIGERANTE')
    print('4- VER PEDIDO')
    print('5- FINALIZAR')
    print('6- SAIR')


def mostrar_cardapio(lista):
    for item in lista:
        valor = f'{item.valor:.2f}'.replace('.', ',')
        print(f'{item.id} - {item.nome}\nR$ {valor}\n')


def buscar_produto(id_produto, *listas):
    for lista in listas:
        for produto in lista:
            if produto.id == id_produto:
                return produto
    return None


def fluxo_categoria(cardapio, pedido):
    while True:
        mostrar_cardapio(cardapio)
        print('1 - Adicionar item')
        print('0 - Voltar ao menu')

        escolha = input('Escolha: ')

        if escolha == '0':
            break
        if escolha != '1':
            print('Opção inválida!')
            continue

        try:
            id_produto = int(input('Digite o ID do produto (0 voltar): '))
            if id_produto == 0:
                continue

            produto = buscar_produto(id_produto, cardapio)
            if produto is None:
                print('Produto inválido!')
                continue

            print(produto.nome)
            print(produto.descricao)

            if not pausa():
                continue

            quantidade = int(input('Quantidade: '))
            if quantidade <= 0:
                print('Quantidade inválida!')
                continue

            pedido.adicionar_item(produto, quantidade)
            print('✅ Item adicionado com sucesso!')

        except ValueError:
            print('Digite apenas números.')

