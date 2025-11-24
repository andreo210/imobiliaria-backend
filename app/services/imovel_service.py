from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.models.amenidade_model import AmenidadeModel
from app.models.foto_imovel_model import FotoImovelModel
from app.models.imovel_amenidade_association import imovel_amenidade_table
from app.models.imovel_model import ImovelModel
from app.models.foto_imovel_model import FotoImovelModel
from app.models.amenidade_model import AmenidadeModel
from sqlalchemy.orm import selectinload
from app.schemas.imovel_schema import (
    ImovelCreate,
    ImovelUpdate,
    ImovelResponse
)
from app.repositories.imovel_repository import ImovelRepository
from app.repositories.foto_imovel_repository import FotoImovelRepository

imovel_repo = ImovelRepository()
foto_repo = FotoImovelRepository()


class ImovelService:

    @staticmethod
    async def listar(db: AsyncSession) -> List[ImovelModel]:
        return await imovel_repo.get_all_full(db)

    @staticmethod
    async def obter(db: AsyncSession, id: int) -> Optional[ImovelModel]:
        return await imovel_repo.get_full(db, id)


    @staticmethod
    async def criar(db: AsyncSession, data: ImovelCreate) -> ImovelModel:
        try:
            # cria imovel
            imovel = ImovelModel(
                titulo=data.titulo,
                descricao=data.descricao,
                preco=data.preco,
                status=data.status,
                tipo_id=data.tipo_id,
                usuario_id=data.usuario_id
            )

            db.add(imovel)
            await db.flush()  # agora imovel.id existe

            # --- INSERÇÃO DE AMENIDADES DIRETO NA TABELA DE ASSOCIAÇÃO ---
            if data.amenidades_ids:
                stmt = insert(imovel_amenidade_table).values([
                    {"imovel_id": imovel.id, "amenidade_id": aid}
                    for aid in data.amenidades_ids
                ])
                await db.execute(stmt)

            # fotos
            if data.fotos:
                for f in data.fotos:
                    foto = FotoImovelModel(imovel_id=imovel.id, url=f.url)
                    db.add(foto)

            await db.commit()

            # retorna o imovel com tudo carregado
            stmt = (
                select(ImovelModel)
                .options(
                    selectinload(ImovelModel.amenidades),
                    selectinload(ImovelModel.fotos),
                    selectinload(ImovelModel.tipo),
                )
                .where(ImovelModel.id == imovel.id)
            )
            result = await db.execute(stmt)
            return result.scalar_one()

        except Exception:
            await db.rollback()
            raise

    @staticmethod
    async def atualizar(db: AsyncSession, id: int, data: ImovelUpdate) -> ImovelModel | None:
        stmt = select(ImovelModel).where(ImovelModel.id == id)
        result = await db.execute(stmt)
        imovel = result.scalar_one_or_none()
        if not imovel:
            return None

        update_data = data.model_dump(exclude_unset=True)
        amenidades_ids = update_data.pop("amenidades_ids", None)

        for field, value in update_data.items():
            setattr(imovel, field, value)

        # atualizar amenidades
        if amenidades_ids is not None:
            stmt = select(AmenidadeModel).where(AmenidadeModel.id.in_(amenidades_ids))
            result = await db.execute(stmt)
            imovel.amenidades = result.scalars().all()

        await db.commit()

        # recarrega com relacionamentos já carregados
        stmt = (
            select(ImovelModel)
            .options(
                selectinload(ImovelModel.amenidades),
                selectinload(ImovelModel.fotos),
                selectinload(ImovelModel.tipo),
            )
            .where(ImovelModel.id == id)
        )
        result = await db.execute(stmt)
        return result.scalar_one_or_none()
