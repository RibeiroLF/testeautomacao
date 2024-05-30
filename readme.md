# Teste de Automação: Login e compra em site

## Descrição

Este script foi desenvolvido como parte de um desafio para automatizar o processo de login e compra no site [SauceDemo](https://www.saucedemo.com). Utilizando o Selenium para controlar o navegador web e BeautifulSoup para analisar dados em formato XML extraídos da página.

## Linguagens e frameworks utilizados
- Python: 3.12
- Selenium: 4.15.2
- BeautifulSoup: 4.15.2

## Etapas
Seguindo as regras do desafio, o script realiza as seguintes etapas:

- 1 - Acessa a página de login do SauceDemo.
- 2 - Salva o conteúdo da página contendo as credenciais de login e senha em um arquivo XML.
- 3 - Extrai os nomes de usuários e a senha do arquivo XML.
- 4 - Seleciona um usuário aleatório, dentre os possíveis, e realiza o login.
- 5 - Adiciona itens ao carrinho.
- 6 - Visualiza o carrinho
- 7 - Prossegue para a finalização da compra especificando o nome e sobrenome do comprador juntamente com um CEP.
- 8 - Finaliza a compra exibindo o valor do total no console.

## Dependências
Além do Python 3.12, Selenium 4.15.2 e BeautifulSoup 4.12.3, o script necessita de algumas dependências adicionais para funcionar:
- GeckoDriver
    - Utilizado para abrir e controlar o Firefox na automação.
    - Certifique-se de que o Geckodriver está instalado e alocado no PATH do sistema.
- Firefox
    - Navegador utilizado para a automação
## Instalação e uso

### Clone o repositório:

```
git clone https://github.com/RibeiroLF/testeautomacao.git
cd repositorio_desejado
```
Instale as dependências:
```
pip install selenium==4.15.2 beautifulsoup4==4.12.3
```
Baixe o Geckodriver e adicione-o ao seu PATH clicando [aqui](https://github.com/mozilla/geckodriver/releases).

### Uso

Apos inicializar o terminal de comando no destino do arquivo. Execute o script principal:
```
python main.py
```
