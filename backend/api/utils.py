from http import HTTPStatus

from django.shortcuts import get_object_or_404
from recipes.models import Recipe
from rest_framework.response import Response
from rest_framework.views import exception_handler
from users.models import Subscription


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response == 401:
        response.data['detail'] = 'Учетные данные не были предоставлены.'
    if response == 404:
        response.data['detail'] = 'Страница не найдена.'
    return response


def func_subscribed(self, obj):
    request = self.context.get('request')
    if not request:
        return True
    if request.user.is_anonymous or obj is None:
        return False
    else:
        return (
            Subscription.objects.filter(
                user=request.user,
                author__id=obj.id
            ).exists()
            and request.user.is_authenticated
        )


def create_favorites_shopcart(request, modelname,
                              serializername, *args, **kwargs):
    recipe_id = kwargs.get('recipe_id')
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if modelname.objects.filter(user=request.user, recipe=recipe).exists():
        return Response(
            'Рецепт уже добавлен',
            status=HTTPStatus.BAD_REQUEST,
        )
    modelname.objects.create(user=request.user, recipe=recipe)
    serializer = serializername(recipe, many=False)
    return Response(data=serializer.data, status=HTTPStatus.CREATED)


def delete_favorites_shopcart(request, modelname, *args, **kwargs):
    recipe_id = kwargs.get('recipe_id')
    recipe = get_object_or_404(Recipe, id=recipe_id)
    get_object_or_404(modelname, user=request.user, recipe=recipe).delete()
    return Response(status=HTTPStatus.NO_CONTENT)
