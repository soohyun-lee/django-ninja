from django.urls import path
from ninja import NinjaAPI
from notice.routes.notices import router as notice_register


viva_notice = NinjaAPI()

viva_notice.add_router('/notice', notice_register, tags=['익명글 등록'])

urlpatterns = [
    path('viva/', viva_notice.urls)
]
