from github.relatorio_usuario import *


class TestClass:
    def test_nome_usuario_foi_preenchido(self):

        entrada = "topo"
        esperado = True

        usuario_teste = Relatorio.valida_usuario_preenchido(self, entrada)

        assert usuario_teste == esperado

    def test_buscar_dados_do_usuario_solicitado(self):

        entrada = "topo"
        esperado = 200

        usuario_teste = Relatorio.buscar_dados_usuario(self, entrada)

        assert usuario_teste.status_code == esperado

    def test_buscar_repositorios_do_usuario_solicitado(self):

        entrada = "topo"
        esperado = False

        usuario_teste = Relatorio.buscar_dados_repositorio_usuario(self, entrada)

        assert usuario_teste != esperado
