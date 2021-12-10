from django.http.response import Http404, JsonResponse
from django.db.models import F
from django.shortcuts import get_object_or_404

from ninja import Router
from pydantic.errors import CallableError
from pydantic.types import Json
from ipware import get_client_ip

from notice.models import Notice, UserLike, Category
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
            password = str(payload.password),
            category = Category.objects.get(name = payload.category)
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
def notice_list(request, category:str = None):
    try:
        # x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        # if x_forwarded_for:
        #     ip = x_forwarded_for.split(',')[0]
        # else:
        #     ip = request.META.get('REMOTE_ADDR')
        ip, is_routable = get_client_ip(request)

        # if ip is not None:
        # 검색 기능 보류
        # if keyword:
        #     notice_list = [{
        #         'id' : notice.id,
        #         'content' : notice.content,
        #         'created_at' : notice.created_at,
        #         'like_count' : notice.like_count,
        #         'is_like' : True if UserLike.objects.filter(user_ip = ip, notice = notice) else False,
        #         'comment_list' : [{
        #             'id' : comment.id,
        #             'comment' : comment.comment,
        #             'created_at' : comment.created_at
        #         } for comment in notice.comment_set.all().order_by('-created_at')]
        #     } for notice in Notice.objects.filter(
        #             content__icontains = keyword
        #         ).order_by('-created_at')]

        #     return 200, NoticeResponseSchema(result=list(notice_list))
        
        notice_list = [{
            'id' : notice.id,
            'content' : notice.content,
            'created_at' : notice.created_at,
            'like_count' : notice.like_count,
            'is_like' : True if UserLike.objects.filter(user_ip = ip, notice = notice) else False,
            'comment_list' : [{
                'id' : comment.id,
                'comment' : comment.comment,
                'created_at' : comment.created_at
            } for comment in notice.comment_set.all().order_by('created_at')]
        } for notice in Notice.objects.filter(
            category = get_object_or_404(Category, name = category)
            ).order_by('-created_at')]
        
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
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        notice = Notice.objects.get(
            id = payload.id
        )
        notice.like_count += 1
        notice.save()

        UserLike.objects.create(
            notice = notice,
            user_ip = ip
        )

        return 200, NoticeListSchema(
            id = notice.id,
            content=notice.content,
            like_count = notice.like_count,
            is_like = True if UserLike.objects.filter(user_ip = ip, notice = notice) else False,
            created_at = notice.created_at,
            comment_count = notice.comment_set.all().count()
        )
    
    except KeyError as e:
        return 404, ErrorSchema(
            message="key error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


@router.put("/nolike", response={200: NoticeListSchema, 400: ErrorSchema})
def notice_register(request, payload : LikeCountSchema):
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        notice = Notice.objects.get(
            id = payload.id
        )
        notice.like_count -= 1
        notice.save()

        UserLike.objects.filter(
            notice = notice,
            user_ip = ip
        ).delete()

        return 200, NoticeListSchema(
            id = notice.id,
            content=notice.content,
            like_count = notice.like_count,
            is_like = True if UserLike.objects.filter(user_ip = ip, notice = notice) else False,
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
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

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
                is_like = True if UserLike.objects.filter(user_ip = ip, notice = notice[0]) else False,
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

        if notice.password == str(payload.password):
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
