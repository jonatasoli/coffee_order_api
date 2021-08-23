# Exemplo
Modelo de design de API feito no Twitch

![Proposta](docs/utterance.png "Proposta")

| Ação      | Verbo  | Url             | Logica de negócio                                                                                                 | Status Code | Status error | Hyperlink                  |
|-----------|--------|-----------------|-------------------------------------------------------------------------------------------------------------------|-------------|--------------|----------------------------|
|   Pedir   |  Post  |    /order   |                                                Criar um novo pedido                                               |     201     |       -      | self,update,cancel,payment |
| Atualizar |   PUT  |  /order/42 |                        Atualiza o pedido, se somente se o status for "Aguardando Pagamento"                       |     200     |      409     | self,update,cancel,payment |
|  Cancelar | DELETE |  /order/42  |            Atualiza o pedido para o status Cancelado, se somente se o status for "Aguardando Pagamento            |     204     |      409     |              -             |
|   Pagar   |   PUT  | /payment/42 | Realiza o pagamento e no sucesso atualiza o status para Pago, se e somente se o status for "Aguardando Pagamento" |     200     |   409, 422   |        self,receipt        |
|  Aguardar |    -   |        -        |                                          Um funcionário prepara o pedido                                          |      -      |       -      |              -             |
|  Receber  | DELETE | /receipt/42 |         Confirma o recebimento atualizando o status para "Entregue", se e somente se o status for "Pronto"        |     204     |      409     |              -             |
|     -     |   GET  |  /order/42  |                                     Retorna a ultima representacao do pedido.                                     |     200     |       -      |      Depende do status     |

## Como instalar

```
poetry install
```

## Entrar na env
```
poetry shell
```

## Executar o projeto
```
uvicorn --factory main:create_app --host 0.0.0.0 --port 8888 --reload
```

## Rodar os testes
```
cd app
pytest -s
```

## Estrutura

### APP
* ext -> estruturas genericas que serao usadas pelos adapters
* migrations -> migracoes
* order -> app com o domain

### Order
* adapters -> camadas externas ao framework e negocio
* domains -> Objetos de negocio
* service -> Regras de negocio
* API -> endpoints
* Locust -> teste de carga
