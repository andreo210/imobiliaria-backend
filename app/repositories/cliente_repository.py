from app.models.cliente_model import ClienteModel


class ClienteRepository:
    def __init__(self):
        super().__init__(ClienteModel)


