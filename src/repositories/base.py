from sqlalchemy.ext.asyncio import AsyncSession
import uuid

class BaseRepository:
    def __init__(self, session: AsyncSession, model):
        self.session = session
        self.model = model

    async def get_by_id(self, item_id: uuid.UUID):
        return await self.session.get(self.model, item_id)

    async def delete(self, item):
        await self.session.delete(item)
        await self.session.commit()
