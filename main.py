from selenium import webdriver
# Import do webdriver para possibilitar abertura do navegador e automatização de processo
import time
# Utilizei a biblioteca time para fazer uso de timer para carregamento completo da página e não ocorrerem erros
from selenium.webdriver.common.by import By 
# Import da classe By que fornece metódos para localização de elementos
from bs4 import BeautifulSoup
# Import da biblioteca beautifulsoup para análise de dados no arquivo XML
import random
# Utilizei esse import para realizar a geração de um número aleátorio para escolha de nome de usuário dentre os possíveis

def iniciar_navegador(url):
    navegador = webdriver.Firefox()
    # Inicialização do navegador
    navegador.get(url)
    # Informa o endereço do site
    time.sleep(1)
    # Temporizador para que o site carregue completamente e não ocorram erros inesperados
    return navegador

def salvar_conteudo_pagina(navegador, xpath, arquivo_xml):
    elemento = navegador.find_element(By.XPATH, xpath)
    # Busca o elemento raíz da página para extrair os dados em formato XML
    conteudo_pagina = elemento.get_attribute('innerHTML')
    with open(arquivo_xml, "w", encoding="utf-8") as arquivo:
        arquivo.write(conteudo_pagina)
    # Gera e carrega um arquivo XML com os dados para usuário e senha

def carregar_credenciais(arquivo_xml):
    with open(arquivo_xml, "r", encoding="utf-8") as arquivo:
        filtro_xml = BeautifulSoup(arquivo.read(), 'html.parser')
    # Reabre o arquivo para leitura e carrega o conteúdo para realizar análise
    return filtro_xml

def extrair_usuarios(filtro_xml):
    usuarios_div = filtro_xml.find('div', {'data-test': 'login-credentials'})
    usuarios_disponiveis = usuarios_div.get_text(separator='\n').strip()
    usuarios_lista = usuarios_disponiveis.split('\n')[1:]
    # Extraindo e gerando uma lista de nomes dos usuários disponíveis no arquivo XML
    usuarios_lista.pop(1)
    # Após alguns testes constatei que os usuário "locked_out_user" está bloqueado para login, por isso ele é removido antes de prosseguir
    usuarios_lista.pop(1)
    # O usuário "problem_user" contém um erro ao adicionar os itens ao carrinho, por isso também será removido
    usuarios_lista.pop(2)
    # O usuário "error_user" também contém um erro ao adicionar itens específicos ao carrinho, por isso também será removido
    return usuarios_lista

def extrair_senhas(filtro_xml):
    senhas_div = filtro_xml.find('div', {'data-test': 'login-password'})
    senhas_disponiveis = senhas_div.get_text(separator=' ').strip()
    senhas_lista = senhas_disponiveis.split(': ')[-1]
    # Extraindo e gerando uma lista de senhas disponíveis no arquivo XML
    return senhas_lista

def realizar_login(navegador, usuario, senha):
    entrada_login = navegador.find_element(By.XPATH, '//*[@id="user-name"]')
    # Seleciona a aba para colocar o nome do usuário
    inserir_login = entrada_login.send_keys(usuario)
    # Faz a inserção do nome do usuário

    entrada_senha = navegador.find_element(By.XPATH, '//*[@id="password"]')
    # Seleciona a aba para colocar a senha do usuário
    inserir_senha = entrada_senha.send_keys(senha)
    # Insere a senha

    botao_login = navegador.find_element(By.XPATH, '//*[@id="login-button"]').click()
    # Realiza o login
    time.sleep(1)

def adicionar_itens_ao_carrinho(navegador):
    itens_xpath = [
        '//*[@id="add-to-cart-test.allthethings()-t-shirt-(red)"]',
        '//*[@id="add-to-cart-sauce-labs-bolt-t-shirt"]',
        '//*[@id="add-to-cart-sauce-labs-bike-light"]'
    ]
    for xpath in itens_xpath:
        navegador.find_element(By.XPATH, xpath).click()
        # Adiciona itens ao carrinho
        time.sleep(1)

def finalizar_compra(navegador, usuario):
    botao_carrinho = navegador.find_element(By.XPATH, '/html/body/div/div/div/div[1]/div[1]/div[3]/a/span').click()
    # Clica no botão para visualização do carrinho
    time.sleep(1)

    navegador.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # Desce até o fim da página para visualização dos itens do carrinho e valor
    time.sleep(1)

    botao_finalizar = navegador.find_element(By.XPATH, '//*[@id="checkout"]').click()
    # Clica no botão de "checkout" para finalização da compra
    time.sleep(1)

    nome_envio = navegador.find_element(By.XPATH, '//*[@id="first-name"]')
    # Seleciona a aba primeiro nome do destinatário
    nome_info = usuario.split('_')
    sobrenome_info = ' '.join(nome_info[1:])
    # Optei por utilizar o mesmo nome de usuario para nome de envio
    # Dividi a string de forma que o primeiro nome seja o índice 0 da lista e os seguintes o sobrenome
    inserir_nome = nome_envio.send_keys(nome_info[0])
    # Insere o nome 

    time.sleep(1)
    sobrenome_envio = navegador.find_element(By.XPATH, '//*[@id="last-name"]')
    # Seleciona a aba de sobrenome do destinatário
    inserir_sobrenome = sobrenome_envio.send_keys(sobrenome_info)
    # Insere o sobrenome

    cep_binario = ''.join(format(ord(c), '08b') for c in usuario)[:8]
    # Na aba de CEP optei por transformar o nome de usuário em seu valor ASCII e após isso converter para uma string binária
    # Como o CEP so possui 8 dígitos a string se trata apenas dos 8 primeiros dígitos
    cep_envio = navegador.find_element(By.XPATH, '//*[@id="postal-code"]')
    # Seleciona a aba pra inserir CEP 
    cep_inserir = cep_envio.send_keys(cep_binario) 
    # Envia o CEP
    time.sleep(1)

    botao_confirmar = navegador.find_element(By.XPATH, '//*[@id="continue"]').click()
    # Clica no botão de confirmação da compra
    time.sleep(1)

    navegador.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    # Desce ao final para visualização do valor da compra

    valor_total = navegador.find_element(By.XPATH, '/html/body/div/div/div/div[2]/div/div[2]/div[8]')
    filtro_valor = valor_total.text.split(': ')
    # Encontra e filtra a guia para exibição de valor total

    print(f'O valor total da compra é: {filtro_valor[1]}')
    # Exibe valor final da compra

    botao_concluir = navegador.find_element(By.XPATH, '//*[@id="finish"]').click()
    # Conclui a compra

def main():
    URL = "https://www.saucedemo.com"
    XPATH_CONTEUDO_PAGINA = '/html/body/div/div/div[2]'
    ARQUIVO_XML = "credenciais.xml"

    navegador = iniciar_navegador(URL)
    salvar_conteudo_pagina(navegador, XPATH_CONTEUDO_PAGINA, ARQUIVO_XML)

    filtro_xml = carregar_credenciais(ARQUIVO_XML)
    usuarios_lista = extrair_usuarios(filtro_xml)
    senha = extrair_senhas(filtro_xml)

    usuario_aleatorio = random.choice(usuarios_lista)
    # Gera um número aleatório que escolhe o nome do usuário, dentre os possíveis

    realizar_login(navegador, usuario_aleatorio, senha)
    adicionar_itens_ao_carrinho(navegador)
    finalizar_compra(navegador, usuario_aleatorio)

if __name__ == "__main__":
    main()
