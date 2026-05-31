from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.models.amenidade_model import AmenidadeModel
from app.models.foto_imovel_model import FotoImovelModel
from app.models.imovel_amenidade_association import imovel_amenidade_table
from app.models.imovel_model import ImovelModel
from sqlalchemy.orm import selectinload
from app.schemas.imovel_schema import (
    ImovelCreate,
    ImovelUpdate,
)
from app.repositories.imovel_repository import ImovelRepository


class ImovelService:
    def __init__(self, repository: ImovelRepository):
        self.repository = repository

    async def listar(self, db: AsyncSession) -> List[ImovelModel]:
        return await self.repository.get_all_full(db)

    async def obter(self, db: AsyncSession, id: int) -> Optional[ImovelModel]:
        return await self.repository.get_full(db, id)

    async def criar(self, db: AsyncSession, data: ImovelCreate) -> ImovelModel:
        try:
            imovel = ImovelModel(
                titulo=data.titulo,
                descricao=data.descricao,
                preco=data.preco,
                status=data.status,
                tipo_id=data.tipo_id,
                usuario_id=data.usuario_id
            )

            db.add(imovel)
            await db.flush()

            if data.amenidades_ids:
                stmt = insert(imovel_amenidade_table).values([
                    {"imovel_id": imovel.id, "amenidade_id": aid}
                    for aid in data.amenidades_ids
                ])
                await db.execute(stmt)

            if data.fotos:
                for f in data.fotos:
                    foto = FotoImovelModel(imovel_id=imovel.id, url=f.url)
                    db.add(foto)

            await db.commit()

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

    async def atualizar(self, db: AsyncSession, id: int, data: ImovelUpdate) -> ImovelModel | None:
        stmt = select(ImovelModel).where(ImovelModel.id == id)
        result = await db.execute(stmt)
        imovel = result.scalar_one_or_none()
        if not imovel:
            return None

        update_data = data.model_dump(exclude_unset=True)
        amenidades_ids = update_data.pop("amenidades_ids", None)

        for field, value in update_data.items():
            setattr(imovel, field, value)

        if amenidades_ids is not None:
            stmt = select(AmenidadeModel).where(AmenidadeModel.id.in_(amenidades_ids))
            result = await db.execute(stmt)
            imovel.amenidades = result.scalars().all()

        await db.commit()

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

    async def excluir(self, db: AsyncSession, id: int) -> bool:
        return await self.repository.deletar(db, id)
