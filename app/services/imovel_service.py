from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.amenidade_model import AmenidadeModel
from app.models.foto_imovel_model import FotoImovelModel
from app.models.imovel_model import ImovelModel
from app.schemas.imovel_schema import (ImovelCreate, ImovelUpdate,ImovelResponse
)
from app.repositories.imovel_repository import ImovelRepository
from app.repositories.foto_imovel_repository import FotoImovelRepository

imovel_repo = ImovelRepository()
foto_repo = FotoImovelRepository()


class ImovelService:

    @staticmethod
    def listar(db: AsyncSession) -> List[ImovelModel]:
        return imovel_repo.get_all_full(db)

    @staticmethod
    def obter(db: AsyncSession, id: int) -> Optional[ImovelModel]:
        return imovel_repo.get_full(db, id)

    @staticmethod
    @staticmethod
    def criar(db: AsyncSession, data: ImovelCreate) -> ImovelModel:
        try:
            # cria o imóvel
            imovel = ImovelModel(
                titulo=data.titulo,
                descricao=data.descricao,
                preco=data.preco,
                status=data.status,
                tipo_id=data.tipo_id,
                usuario_id=data.usuario_id
            )
            db.add(imovel)
            db.flush()  # garante que imovel.id já existe sem commit

            # amenidades
            if data.amenidades_ids:
                stmt = select(AmenidadeModel).where(AmenidadeModel.id.in_(data.amenidades_ids))
                result = db.execute(stmt)
                imovel.amenidades = result.scalars().all()

            # fotos
            if data.fotos:
                for f in data.fotos:
                    foto = FotoImovelModel(imovel_id=imovel.id, url=f.url)
                    db.add(foto)

            db.commit()
            db.refresh(imovel)
            return imovel

        except Exception:
            db.rollback()
            raise

    @staticmethod
    def atualizar(db: AsyncSession, id: int, data: ImovelUpdate) -> Optional[ImovelModel]:
        imovel = imovel_repo.get(db, id)
        if not imovel:
            return None

        # aplica campos atualizáveis
        update_data = data.model_dump(exclude_unset=True)
        amenidades_ids = update_data.pop("amenidades_ids", None)

        for field, value in update_data.items():
            setattr(imovel, field, value)

        # atualizar amenidades, se enviadas
        if amenidades_ids is not None:
            stmt = select(AmenidadeModel).where(AmenidadeModel.id.in_(amenidades_ids))
            result = db.execute(stmt)
            imovel.amenidades = result.scalars().all()

        db.commit()
        db.refresh(imovel)

        return imovel_repo.get_full(db, id)

    @staticmethod
    def excluir(db: AsyncSession, id: int) -> bool:
        return imovel_repo.delete(db, id)
