import requests
import json


class Relatorio:

    def relatorio_usuario(self):

        usuario = input("Digite qual usuário você deseja pesquisar: ").replace(' ', '').lower()

        if not Relatorio.valida_usuario_preenchido(self, usuario):
            Relatorio.relatorio_usuario(self)
            return False

        # Busco os dados do usuário solicidado
        dados_usuario = Relatorio.buscar_dados_usuario(self, usuario)

        if not dados_usuario:
            Relatorio.relatorio_usuario(self)
            return False

        dados_usuario = dados_usuario.json()

        # Crio o arquivo do relatório e escrevo os dados encontrados do usuário solicitado
        Relatorio.escreve_dados_usuario_relatorio(self, usuario, dados_usuario)

        # Busco os repositórios do usuário solicitado
        repositorios = Relatorio.buscar_dados_repositorio_usuario(self, usuario)

        # Atualizo o arquivo do relatório com os dados encontrados dos repositórios do usuário solicitado
        Relatorio.escreve_dados_repositorios_usuario_relatorio(self, usuario, repositorios)

        print(f"Relatório '{usuario}.txt' criado com sucesso! \n")

        # Finalizo a aplicação
        Relatorio.finalizar_app(self)

    def valida_usuario_preenchido(self, usuario):

        # Valido se o usuário foi preenchido ou não
        if not usuario:
            print(f"Por favor, especifique um usuário... \n")
            return False

        return True

    def escreve_dados_usuario_relatorio(self, usuario, dados_usuario):

        # Trato os dados recuperados da busca
        nome = "Nome não especificado" if dados_usuario["name"] is None else dados_usuario["name"]
        perfil = "Perfil não especificado" if dados_usuario["login"] is None else dados_usuario["login"]
        repositorios_publicos = "Nº de repos não especificado" if dados_usuario["public_repos"] is None else \
        dados_usuario[
            "public_repos"]
        seguidores = 0 if dados_usuario["followers"] is None else dados_usuario["followers"]
        seguindo = 0 if dados_usuario["following"] is None else dados_usuario["following"]

        # Nomeio, crio o arquivo e preencho as informações correspondente ao relatório do usuário
        filename = usuario + ".txt"
        f = open(filename, "w")
        f.write("Nome: " + nome + "\n")
        f.write("Perfil: " + perfil + "\n")
        f.write("Número de repositórios públicos: " + str(repositorios_publicos) + "\n")
        f.write("Seguidores: " + str(seguidores) + "\n")
        f.write("Seguindo: " + str(seguindo) + "\n")

        f.close()

    def escreve_dados_repositorios_usuario_relatorio(self, usuario, repositorios):

        filename = usuario + ".txt"
        f = open(filename, "a")

        # Valido se existe repositórios disponíveis
        if repositorios:

            # Escrevo a lista dos repositórios disponíveis
            f.write("Lista de repositórios: " + "\n")
            for repositorio in repositorios:
                f.write(" > " + repositorio["name"] + "\n")
        else:
            # Informo que usuário não possui lista dos repositórios disponível
            f.write(f"Usuário {usuario} não possui uma lista de repositórios disponível!")

        f.close()

    def buscar_dados_usuario(self, usuario):

        url = "https://api.github.com/users/" + usuario

        print(f"Buscando usuário: {url}")

        # Busco os dados correspondentes ao usuário solicitado
        dados_usuario = requests.get(url)

        # Verifico se o status code é diferente de 200, para saber se o usuário foi ou não encontrado
        if dados_usuario.status_code != 200:

            dados_usuario = dados_usuario.json()

            if dados_usuario["message"]:

                mensagem = dados_usuario["message"]
                print(f"{mensagem} \n")
                Relatorio.finalizar_app(self)

            else:
                print(f"Usuário '{usuario}' não existe! \n")

            return False

        return dados_usuario

    def buscar_dados_repositorio_usuario(self, usuario):

        url = "https://api.github.com/users/" + usuario

        url_repositorios = url + "/repos"

        # Busco os repositórios correspondentes ao usuário solicitado
        repositorios = requests.get(url_repositorios).json()

        if len(repositorios) <= 0:
            print(f"Usuário '{usuario}' não possui repositórios disponíveis! \n")
            return False

        return repositorios

    def finalizar_app(self):

        # Questiono se o usuário deseja finalizar ou não a busca de usuários
        nova_pesquisa = input("Realizar nova pesquisa? [Sim/Não]: ").replace(' ', '').lower()

        if nova_pesquisa == 'sim':

            # Reinício do processo de busca da aplicação
            Relatorio.relatorio_usuario(self)

        else:

            # Valido se a opção selecionada é válida
            if nova_pesquisa != 'não':
                print("Opção desconhecida!")
                Relatorio.finalizar_app(self)

            exit()