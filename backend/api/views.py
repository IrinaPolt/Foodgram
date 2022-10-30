from http import HTTPStatus
from os import path

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Purchase, Recipe,
                            RecipeIngredient, Tag)
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import Subscription, User

from .filters import IngredientFilter, RecipeFilter
from .mixins import CreateDestroyViewSet, ListRetrieveViewSet
from .pagination import PageLimitPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeCreateUpdateSerializer, RecipeSerializer,
                          RecipeShortSerializer, ShoppingCartSerializer,
                          SubscriptionSerializer, TagSerializer,
                          UserSerializer)
from .utils import create_favorites_shopcart, delete_favorites_shopcart

app_path = path.realpath(path.dirname(__file__))
font_path = path.join(app_path, 'fonts/timesnewromanpsmt.ttf')


class TagsViewSet(ListRetrieveViewSet):
    queryset = Tag.objects.all()
    pagination_class = None
    serializer_class = TagSerializer
    permission_classes = [permissions.AllowAny, ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly, ]
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    pagination_class = PageLimitPagination

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return RecipeSerializer
        else:
            return RecipeCreateUpdateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = PageLimitPagination


class IngredientViewSet(ListRetrieveViewSet):
    queryset = Ingredient.objects.all()
    permission_classes = [permissions.AllowAny, ]
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, IngredientFilter]
    pagination_class = None
    search_fields = ['^name', ]


class SubscriptionViewSet(ListRetrieveViewSet):
    serializer_class = SubscriptionSerializer

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)


class SubscribeViewSet(CreateDestroyViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=author_id)
        if author == request.user:
            return Response(
                'Нельзя подписаться на себя',
                status=HTTPStatus.BAD_REQUEST
            )
        if Subscription.objects.filter(
                author=author, user=self.request.user).exists():
            return Response(
                'Вы уже подписаны на данного автора',
                status=HTTPStatus.BAD_REQUEST
            )
        Subscription.objects.create(author=author, user=self.request.user)
        subscription = get_object_or_404(
            Subscription,
            author=author,
            user=self.request.user
        )
        serializer = SubscriptionSerializer(subscription, many=False)
        return Response(data=serializer.data, status=HTTPStatus.CREATED)

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('user_id')
        author = get_object_or_404(User, id=author_id)
        get_object_or_404(
            Subscription,
            author=author,
            user=self.request.user
        ).delete()
        return Response(status=HTTPStatus.NO_CONTENT)


class FavoriteViewSet(CreateDestroyViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        return create_favorites_shopcart(
            request, Favorite, RecipeShortSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return delete_favorites_shopcart(request, Favorite, *args, **kwargs)


class DownloadShoppingCartViewSet(APIView):
    permission_classes = [permissions.IsAuthenticated, ]

    @staticmethod
    def canvas_method(shopping_list):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename = "shopping_cart.pdf"')
        begin_position_x, begin_position_y = 100, 650
        sheet = canvas.Canvas(response, pagesize=A4)
        pdfmetrics.registerFont(
            TTFont('TNR', font_path)
        )
        sheet.setFont('TNR', 32)
        sheet.setTitle('Список покупок')
        sheet.drawString(
            begin_position_x,
            begin_position_y + 40,
            'Список покупок: '
        )
        sheet.setFont('TNR', 20)
        for number, item in enumerate(shopping_list, start=1):
            if begin_position_y < 100:
                begin_position_y = 700
                sheet.showPage()
                sheet.setFont('TNR', 20)
            sheet.drawString(
                begin_position_x,
                begin_position_y,
                f'{number}.  {item["ingredient__name"]} - '
                f'{item["ingredient_total"]}'
                f' {item["ingredient__measurement_unit"]}'
            )
            begin_position_y -= 30
        sheet.showPage()
        sheet.save()
        return response

    def get(self, request):
        result = RecipeIngredient.objects.filter(
            recipe__recipeincart__user=request.user).values(
            'ingredient__name', 'ingredient__measurement_unit').order_by(
                'ingredient__name').annotate(ingredient_total=Sum('amount'))
        return self.canvas_method(result)


class ShoppingCartViewSet(CreateDestroyViewSet):
    serializer_class = ShoppingCartSerializer
    permission_classes = [permissions.IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        return create_favorites_shopcart(
            request, Purchase, RecipeShortSerializer, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return delete_favorites_shopcart(request, Purchase, *args, **kwargs)
