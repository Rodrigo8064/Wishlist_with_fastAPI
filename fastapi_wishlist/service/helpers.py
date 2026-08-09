from sqlalchemy.ext.asyncio import AsyncSession


class UserConflictError(Exception):
    pass


class NotFoundError(Exception):
    def __init__(self, resource_name: str):
        self.resource_name = resource_name
        super().__init__(f'{resource_name} não encontrado')


async def save_object(db: AsyncSession, db_object):
    db.add(db_object)
    await db.commit()
    await db.refresh(db_object)

    return db_object


async def update_object(db: AsyncSession, db_object):
    await db.commit()
    await db.refresh(db_object)

    return db_object


async def delete_object(db: AsyncSession, db_object):
    await db.delete(db_object)
    await db.commit()


async def get_object(
    db: AsyncSession, db_model, object_id: int, resource_name: str
):
    db_object = await db.get(db_model, object_id)
    if not db_object:
        raise NotFoundError(resource_name)
    return db_object
