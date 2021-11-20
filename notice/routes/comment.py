from django.http.response import Http404, JsonResponse
from django.shortcuts import get_list_or_404
from django.db.models import F

from ninja import Router

from notice.models import Notice, User, Comment
from notice.schema import (
    ErrorSchema,
    CommentListScheme,
    CreateComment,
    CommentResponseSchema,
    SuccessSchema,
    CommentDeleteSchema
)


router = Router()

@router.post("", response={200: CommentListScheme, 400: ErrorSchema})
def comment_register(request, payload : CreateComment):
    try:
        notice_comment = Comment.objects.create(
            notice_id = payload.notice_id,
            password = payload.password,
            comment = payload.comment
        )

        return 200, CommentListScheme(
            id = notice_comment.id,
            comment = notice_comment.comment
        )
    
    except KeyError as e:
        return 404, ErrorSchema(
            message="key error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


@router.get("", response={200:CommentResponseSchema, 400: ErrorSchema})
def comment_list(request, notice_id:int):
    try:
        a = Comment.objects.filter(notice_id = notice_id)
        print(a)
        return 200, CommentResponseSchema(result=list(Comment.objects.filter(
            notice_id=notice_id
        )))
    
    except ValueError as e:
        return 404, ErrorSchema(
            message="value error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


@router.delete("", response={200: SuccessSchema, 400: ErrorSchema})
def comment_delete(request, payload : CommentDeleteSchema):
    try:
        comment = Comment.objects.get(
            id = payload.id
        )

        if comment.password == payload.password:
            comment.delete()
            
            return 200, SuccessSchema(
                message = "삭제 성공"
            )
        
        raise ValueError('비밀번호가 일치하지 않습니다.')

    except ValueError as value_error:
        return 400, ErrorSchema(
            message="값을 다시 확인해주세요.",
            error_code=f"400{'2'.zfill(4)}",
            detail=str(value_error),
        )
    
    except KeyError as e:
        return 404, ErrorSchema(
            message="key error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )
