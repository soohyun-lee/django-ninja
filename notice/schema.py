import datetime
from typing import List
from django.db.models.fields import DateTimeField, Field
from ninja.schema import Schema

class NoticeSchema(Schema):
    password: str = None
    content: str = None
    category: str = None

    class Config:
        schema_extra = {
        "example": {
            "password": "비밀번호",
            "content": "내용",
            "category": "댄에게 말해요 / 대나무숲 (둘 중 하나의 스트링으로 전달)",
        }
    }

class NoticeEditSchema(Schema):
    id: int = None
    password: str = None
    content: str = None
    user_id: str = None
    
class UserSchema(Schema):
    email: str = None


class LikeCountSchema(Schema):
    id: int = None
    user_id: int = None


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
    id: str = None


class UserAuthSchema(Schema):
    message: str
    user_id: int = None


class DeleteSchema(Schema):
    id: int = None
    password: str = None


class AuthCheckSchema(Schema):
    email: str = None
    code: str = None
    fcm_token: str = None


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
    is_like: bool = None
    comment_list : List[CommentListSchema] = None


class NoticeResponseSchema(Schema):
    result : List[NoticeListSchema] = None


class SignupSchema(Schema):
    email: str = None