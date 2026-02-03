class Produto:
    def __init__(self,id, nome, valor,descricao,imagem):
        self.id = id
        self.nome = nome
        self.valor = valor
        self.descricao = descricao
        self.imagem = imagem


class ItemPedido:
    def __init__(self,produto,quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def subtotal(self):
        return self.produto.valor * self.quantidade

class Pedido:
    def __init__(self):
        self.itens=[]

    def adicionar_item(self,produto,quantidade):
        self.itens.append(ItemPedido(produto,quantidade))

    def total(self):
        return sum(item.subtotal() for item in self.itens)

    def imprime(self):
        if not self.itens:
            print('Nenhum item no pedido.')
            return

        print('\n🧾 PEDIDO ATUAL')
        for item in self.itens:
            print(f'- {item.produto.nome} x{item.quantidade} '
                  f'R$ {item.subtotal():.2f}')
            print(f'\nTotal: R$ {self.total():.2f}')
