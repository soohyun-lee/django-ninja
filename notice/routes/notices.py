from django.http.response import Http404, JsonResponse
from django.shortcuts import get_list_or_404
from django.db.models import F

from ninja import Router
from pydantic.types import Json

from notice.models import Notice, User
from notice.schema import (
    NoticeListSchema, 
    NoticeSchema, 
    ErrorSchema,
    NoticeResponseSchema,
    LikeCountSchema,
    SuccessSchema,
    DeleteSchema,
    NoticeEditSchema,
    SearchSchema
)


router = Router()

@router.post("", response={200: NoticeListSchema, 400: ErrorSchema})
def notice_register(request, payload : NoticeSchema):
    try:
        notice = Notice.objects.create(
            content = payload.content,
            password = payload.password
        )

        return 200, NoticeListSchema(
            id = notice.id,
            content=payload.content,
            like_count = notice.like_count,
            created_at = notice.created_at,
            comment_count = notice.comment_set.all().count()
        )
    
    except KeyError as e:
        return 404, ErrorSchema(
            message="key error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


@router.get("", response={200:NoticeResponseSchema, 400: ErrorSchema})
def notice_list(request, keyword:str = None):
    try:
        if keyword:
            notice_list = [{
                'id' : notice.id,
                'content' : notice.content,
                'created_at' : notice.created_at,
                'like_count' : notice.like_count,
                'comment_list' : [{
                    'id' : comment.id,
                    'comment' : comment.comment
                } for comment in notice.comment_set.all()]
            } for notice in Notice.objects.filter(
                    content__icontains = keyword
                )]

            return 200, NoticeResponseSchema(result=list(notice_list))
        
        notice_list = [{
            'id' : notice.id,
            'content' : notice.content,
            'created_at' : notice.created_at,
            'like_count' : notice.like_count,
            'comment_list' : [{
                'id' : comment.id,
                'comment' : comment.comment
            } for comment in notice.comment_set.all()]
        } for notice in Notice.objects.all()]
        
        return 200, NoticeResponseSchema(result=list(notice_list))
        
    except ValueError as e:
        return 404, ErrorSchema(
            message="value error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


@router.post("/like", response={200: NoticeListSchema, 400: ErrorSchema})
def notice_register(request, payload : LikeCountSchema):
    try:
        notice = Notice.objects.get(
            id = payload.id
        )
        notice.like_count += 1
        notice.save()

        return 200, NoticeListSchema(
            id = notice.id,
            content=notice.content,
            like_count = notice.like_count,
            created_at = notice.created_at,
            comment_count = notice.comment_set.all().count()
        )
    
    except KeyError as e:
        return 404, ErrorSchema(
            message="key error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


@router.put("", response={200: NoticeListSchema, 400: ErrorSchema})
def notice_register(request, payload : NoticeEditSchema):
    try:
        notice = Notice.objects.filter(
            id = payload.id
        )

        if notice[0].password == payload.password:
            notice.update(
                content = payload.content
            )

            return 200, NoticeListSchema(
                id = payload.id,
                content=payload.content,
                like_count = notice[0].like_count,
                created_at = notice[0].created_at,
                comment_count = notice[0].comment_set.all().count()
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


@router.put("/delete", response={200: SuccessSchema, 400: ErrorSchema})
def notice_register(request, payload : DeleteSchema):
    try:
        notice = Notice.objects.get(
            id = payload.id
        )

        if notice.password == payload.password:
            notice.delete()
            
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
