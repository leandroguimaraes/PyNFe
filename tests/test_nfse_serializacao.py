
import pyxb.namespace
from pynfe.entidades.cliente import Cliente
from pynfe.entidades.emitente import Emitente
from pynfe.entidades.notafiscal import NotaFiscalServico
from pynfe.entidades.servico import Servico
from pynfe.processamento.serializacao import SerializacaoNfse
from pynfe.utils import obter_codigo_por_municipio
from pynfe.utils.flags import (
    CODIGO_BRASIL,
)
from decimal import Decimal
import datetime
import re


class SerializacaoNFSeConfigTest:
    def __init__(self, certificado: str, senha: str, homologacao: bool):
        self.certificado = certificado
        self.senha = senha
        self.homologacao = homologacao


class SerializacaoNFSeTest:

    @staticmethod
    def get_config() -> SerializacaoNFSeConfigTest:
        return SerializacaoNFSeConfigTest(
            "./tests/certificado.pfx",
            bytes("123456", "utf-8"),
            True
        )

    @staticmethod
    def get_notafiscal_servico() -> NotaFiscalServico:
        servico = Servico(
            valor_servico=Decimal('100.00'),
            iss_retido=1,  # 1 - Sim; 2 - Não
            item_lista='0101',
            discriminacao='Mensalidade',
            codigo_municipio=obter_codigo_por_municipio(
                'Pedro Leopoldo', 'MG'),
            # Dados opcionais
            codigo_cnae=6201501,
            codigo_tributacao_municipio='1234',
            valor_deducoes=Decimal('10.00'),
            valor_pis=Decimal('10.00'),
            valor_confins=Decimal('10.00'),
            valor_inss=Decimal('10.00'),
            valor_ir=Decimal('10.00'),
            valor_csll=Decimal('10.00'),
            valor_iss=Decimal('10.00'),
            valor_iss_retido=Decimal('10.00'),
            valor_liquido=Decimal('10.00'),
            outras_retencoes=Decimal('10.00'),
            base_calculo=Decimal('10.00'),
            aliquota=Decimal('10.00'),
            desconto_incondicionado=Decimal('10.00'),
            desconto_condicionado=Decimal('10.00')
        )

        return NotaFiscalServico(
            identificador='50',
            data_emissao=datetime.datetime.now(),
            servico=servico,
            emitente=SerializacaoNFSeTest._get_emitente(),
            cliente=SerializacaoNFSeTest._get_destinatario(),
            # Optante Simples Nacional
            simples=1,     # 1-Sim; 2-Não
            # 1 – Tributação no município 2 - Tributação fora do município 3 - Isenção 4 - Imune
            natureza_operacao=1,
            # 5 –Exigibilidade suspensa por decisão judicial 6 – Exigibilidade suspensa por procedimento administrativo
            # regime_especial=1, # Regime Especial de Tributação: 1 – Microempresa municipal 2 - Estimativa
            # 3 – Sociedade de profissionais 4 – Cooperativa 5 - Microempresário Individual (MEI)
            # 6 - Microempresário e Empresa de Pequeno Porte (ME EPP)
            incentivo=2,   # Incentivador Cultural # 1-Sim; 2-Não
            serie='A1',
            tipo='1'
        )

    @staticmethod
    def serializa_nfse(nfse: NotaFiscalServico, autorizador: str) -> str:
        serializador = SerializacaoNfse(autorizador)
        xml = serializador.gerar(nfse)
        return xml

    # TODO: assinatura digital
    # @staticmethod
    # def assina_xml(config: SerializacaoNFSeConfigTest, nfse_xml: str):
    #     a1 = AssinaturaA1(config.certificado, config.senha)
    #     xml = a1.assinar(nfse_xml, True)
    #     return xml

    @staticmethod
    def strip_xml(xml: str) -> str:
        return re.sub(r">\s+<", "><", xml.replace("\n", "").strip())

    @staticmethod
    def limpa_namespace() -> None:
        # Limpa o Namespace para não gerar conflito com outros testes
        pyxb.namespace.Namespace._Namespace__Registry.clear()

    # TODO: Testa a validação do XML com os schemas XSD
    # @staticmethod
    # def validacao_com_xsd_do_xml_gerado_sem_processar(self, nfse_xml: str, nfse_xml_assinado: str, xsd_file: str, xsd_folder: str) -> None:
    #     validacao = Validacao()
    #     xsd_nfse = validacao.get_xsd(
    #         xsd_file=xsd_file, xsd_folder=xsd_folder
    #     )

    #     validacao.validar_etree(
    #         xml_doc=etree.fromstring(nfse_xml), xsd_file=xsd_nfse, use_assert=True
    #         # TODO: assinatura digital
    #         xml_doc=nfse_xml_assinado, xsd_file=xsd_nfse, use_assert=True
    #     )

    @staticmethod
    def _get_emitente() -> Emitente:
        return Emitente(
            cnpj='99999999999999',
            inscricao_municipal='000000'
        )

    @staticmethod
    def _get_destinatario() -> Cliente:
        return Cliente(
            razao_social='NF-E EMITIDA EM AMBIENTE DE HOMOLOGACAO - SEM VALOR FISCAL',
            tipo_documento='CNPJ',                          # CPF ou CNPJ
            # apenas os numeros do CPF ou CNPJ
            numero_documento='99999999999999',
            inscricao_municipal='1234',                     # opcional
            endereco_logradouro='Rua tal',
            endereco_numero='0',
            endereco_complemento='Ao lado de lugar nenhum',  # opcional
            endereco_bairro='Centro',
            endereco_cod_municipio='123',
            endereco_uf='MG',
            endereco_cep='33257010',
            endereco_pais=CODIGO_BRASIL,
            endereco_telefone='12365478945',                # opcional
            email='nome@email.com.br'                       # opcional
        )
