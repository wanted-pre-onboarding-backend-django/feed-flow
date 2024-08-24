import requests
from django.http import Http404
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from article.models import Article
from article.utils.article_site_dict import article_site_dict


class ArticleShareAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        GET : /articles/:id/share/
        게시물 공유 버튼 클릭 시, share_cnt 1씩 증가

        TODO: 나중에 에러 메시지 한 파일에 모아서 관리할 것
        TODO: 해당하는 사이트의 공유 기능과 연결하기
        """
        try:
            # path param으로 article_id 추출
            article_id = kwargs.get("article_id")

            # 게시글 id가 전달되지 않을 시, 오류
            if not article_id:
                raise ValidationError()

            # 해당하는 article 객체 조회
            # 없을 시, 404 Error 발생
            try:
                article = get_object_or_404(Article, id=article_id)
            except Http404:
                return Response(
                    {"msg": "해당하는 게시글이 없습니다."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            # 외부 api 요청용 url 제작
            # 현재는 주석 처리
            # url = ""
            # if article.type in article_site_dict:
            #     url = article_site_dict[article.type] + f"/share/{article.content_id}"
            # else:
            #     return Response(
            #         {"msg": "존재하지 않는 사이트입니다."},
            #         status=status.HTTP_400_BAD_REQUEST,
            #     )

            # 외부 api 호출
            # response = requests.post(url)
            # if response.status_code != 200:
            #     return Response(
            #         {"msg": "해당 사이트와의 공유 작업에 실패했습니다."},
            #         status=status.HTTP_500_INTERNAL_SERVER_ERROR
            #     )

            # share_cnt 증가
            article.share_cnt += 1
            article.save()

            # 성공 시, 200 응답
            return Response(status=status.HTTP_200_OK)

        # 에러 처리
        except ValidationError as e:
            # 잘못된 요청 시(400)
            return Response(
                {"msg": f"{e.detail} 게시글 번호가 필요합니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except Exception as e:
            # 그 외 예외 처리(500)
            return Response(
                {"msg": f"{str(e)} 오류가 발생했습니다. 다시 시도해주세요."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
