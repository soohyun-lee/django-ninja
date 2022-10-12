import random
import string
import random

from django.http.response import Http404, JsonResponse
from django.db.models import F
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage

from ninja import Router
from pydantic.errors import CallableError
from pydantic.types import Json

from notice.models import Notice, UserLike, Category, User
from notice.schema import (
    NoticeListSchema, 
    NoticeSchema, 
    ErrorSchema,
    NoticeResponseSchema,
    LikeCountSchema,
    SuccessSchema,
    DeleteSchema,
    NoticeEditSchema,
    UserSchema,
    AuthCheckSchema,
    UserAuthSchema
)

router = Router()


@router.post("/user", response={200: SuccessSchema, 400: ErrorSchema})
def user_register(request, payload : UserSchema):
    try:
        user = get_object_or_404(User, email = payload.email)
        if user:
            code = random.sample(range(0,9),4)
            auth_code = "".join(map(str, code))
            
            number_of_strings = 5
            length_of_string = 8
            for x in range(number_of_strings):
                auth_code = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_of_string))

            user.auth_code = auth_code
            user.save()

            email = EmailMessage(
                '대나무숲 인증 메일',
                f'대나무 숲 인증 코드를 입력해주세요 : \n {auth_code}',
                to=[f"{payload.email}"])
            
            email_send = email.send()
            
            if email_send == 1:
                return 200, SuccessSchema(
                    message = "인증 메일 발송 성공",
                )
            else:
                return 400, ErrorSchema(
                    message="이메일 발송 실패",
                    error_code=f"400{'1'.zfill(4)}",
                    detail="이메일 발송 실패",
                )
        else:
            return 400, ErrorSchema(
                message="Does not exist User",
                error_code=f"400{'1'.zfill(4)}",
                detail="Does not exist User",
            )

    except KeyError as e:
        return 404, ErrorSchema(
            message="key error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


@router.post("/user/check", response={200: UserAuthSchema, 400: ErrorSchema})
def auth_check(request, payload : AuthCheckSchema):
    try:
        user = get_object_or_404(User, email=payload.email)
        if user.auth_code == payload.code:
            user.fcm_token = payload.fcm_token
            user.save()

            return 200, UserAuthSchema(
                message = "인증 성공",
                user_id = user.id
            )

        else:
            return 400, ErrorSchema(
                message="인증번호가 다릅니다",
                error_code=f"400{'1'.zfill(4)}",
                detail="인증번호가 다릅니다",
            )

    except KeyError as e:
        return 404, ErrorSchema(
            message="key error",
            error_code=f"400{'1'.zfill(4)}",
            detail=str(e),
        )


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
            like_count = notice.userlike_set.all().count(),
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
def notice_list(request, category: str, user_id: str):
    try:
        
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
            'like_count' : notice.userlike_set.all().count(),
            'is_like' : True if UserLike.objects.filter(user_id = user_id, notice = notice) else False,
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
        notice = Notice.objects.get(
            id = payload.id
        )

        userlike = UserLike.objects.filter(
            notice_id = payload.id,
            user_id = payload.user_id
        )
        if userlike:
            return 400, ErrorSchema(
                message="like error",
                error_code=f"400{'1'.zfill(4)}",
                detail="like error",
            )
        else:
            UserLike.objects.create(
                notice_id = payload.id,
                user_id = payload.user_id
            )
        
            return 200, NoticeListSchema(
                id = notice.id,
                content=notice.content,
                like_count = notice.userlike_set.all().count(),
                is_like = True if UserLike.objects.filter(
                    user_id = payload.user_id, notice = notice) else False,
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
        notice = Notice.objects.get(
            id = payload.id
        )
        
        UserLike.objects.filter(
            notice = payload.id,
            user = payload.user_id
        ).delete()

        return 200, NoticeListSchema(
            id = notice.id,
            content=notice.content,
            like_count = notice.userlike_set.all().count(),
            is_like = True if UserLike.objects.filter(
                user_id = payload.user_id, notice = notice) else False,
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
                like_count = notice[0].userlike_set.all().count(),
                is_like = True if UserLike.objects.filter(
                    user_id = payload.user_id, notice = notice[0]) else False,
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

