from abc import ABCMeta
from typing import Any, Generic, Type, TypeVar, List

from fastapi.encoders import jsonable_encoder
from loguru import logger
from pydantic import BaseModel, parse_obj_as
from sqlalchemy.exc import DataError, DatabaseError, DisconnectionError, IntegrityError
from sqlalchemy.sql.expression import select, text

from ext.db.base_class import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(
    Generic[ModelType, CreateSchemaType, UpdateSchemaType], metaclass=ABCMeta
):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update (CRU).
        **Parameters**
        * `model`: A SQLAlchemy model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    def obj_in_to_db_obj(self, obj_in: Any):
        obj_in_data = jsonable_encoder(obj_in)
        return self.model(**obj_in_data)

    def obj_in_to_db_obj_attrs(self, obj_in: Any, db_obj: Any):
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        return db_obj


    async def get(self, obj_id: Any):
        try:
            db_obj = await self.model.id == obj_id
            response = None
            if db_obj:
                response = self.Meta.response_get_type.from_orm(db_obj)
            return response

        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e

    async def create(self, obj_in: CreateSchemaType) -> ModelType:
        try:
            data_db = self.obj_in_to_db_obj(obj_in=obj_in)
            async with self.Meta.session() as db:
                db.add(data_db)
                await db.commit()
                response = self.Meta.response_create_type.from_orm(data_db)

            return response
        except (DataError, DatabaseError, DisconnectionError, IntegrityError) as err:
            logger.error(f"SQLAlchemy error {err}")
        except Exception as e:
            logger.error(f"Error in dao {e}")
            raise e
