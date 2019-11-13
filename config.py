class Config(object):
    """Configuração comum"""


class DevelopmentConfig(object):
    """Configuração de Desenvolvimento"""

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(object):
    """Configuração de Produção"""

    DEBUG = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
