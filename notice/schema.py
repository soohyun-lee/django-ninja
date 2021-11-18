# import 
import datetime
from typing import List, Optional
from django.db.models.fields import DateTimeField
from ninja.schema import Schema

class NoticeSchema(Schema):
    id: int = None
    password: str = None
    content: str = None


class LikeCountSchema(Schema):
    id: int = None


class NoticeListSchema(Schema):
    id: int = None
    content: str = None
    created_at: datetime.datetime = None
    like_count: int


class NoticeResponseSchema(Schema):
    result : List[NoticeListSchema] = None


class ErrorSchema(Schema):
    message : str
    error_code : int
    detail : str = None


class SuccessSchema(Schema):
    message : str


class DeleteSchema(Schema):
    id: int = None
    password: str = None
