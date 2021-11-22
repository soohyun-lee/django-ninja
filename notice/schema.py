import datetime
from typing import List
from django.db.models.fields import DateTimeField, Field
from ninja.schema import Schema

class NoticeSchema(Schema):
    password: str = None
    content: str = None


class NoticeEditSchema(Schema):
    id: int = None
    password: str = None
    content: str = None


class LikeCountSchema(Schema):
    id: int = None


# class NoticeListSchema(Schema):
#     id: int = None
#     content: str = None
#     created_at: datetime.datetime = None
#     like_count: int
#     id: int = None
#     comment: str = None


# class NoticeResponseSchema(Schema):
#     result : List[NoticeListSchema] = None


class ErrorSchema(Schema):
    message : str
    error_code : int
    detail : str = None


class SuccessSchema(Schema):
    message : str


class DeleteSchema(Schema):
    id: int = None
    password: str = None


class SearchSchema(Schema):
    keyword: str = None


class CommentListScheme(Schema):
    id: int = None
    comment: str = None
    created_at: datetime.datetime = None



class CommentResponseSchema(Schema):
    result : List[CommentListScheme] = None


class CreateComment(Schema):
    notice_id: int = None
    comment: str = None

    class Config:
        schema_extra = {
            "example": {
                "notice_id": "게시글 id - integer",
                "comment": "댓글",
            }
        }

class CommentDeleteSchema(Schema):
    id: int = None

    class Config:
        schema_extra = {
        "example": {
            "id": "댓글 고유 id - integer",
        }
    }

class CommentListSchema(Schema):
    id : int
    comment : str
    created_at: datetime.datetime


class NoticeListSchema(Schema):
    id: int = None
    content: str = None
    created_at: datetime.datetime = None
    like_count: int
    comment_list : List[CommentListSchema] = None


class NoticeResponseSchema(Schema):
    result : List[NoticeListSchema] = None