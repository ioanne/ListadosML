from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.generic import TemplateView
from apps.applicationML.sdk.lib.meli import Meli
from apps.applicationML.models import Application
from apps.applicationML.forms import SelectAppForm

import json

def top_product_list(order_by, meli, access_token):
    category_id = 'MLA411116'
    products = meli.get(
                '/sites/MLA/search?category={}&limit=200'
                .format(category_id))
    products = json.loads(products.text)

    count = 0
    if products['paging']['total'] > 200:
        
        while len(products['results']) < products['paging']['total']:
            count += 1
            new_products = meli.get(
                            '/sites/MLA/search?category={}&limit=200&offset={}'
                            .format(category_id, 200*count))
            new_products = json.loads(new_products.text)
            products['results'] += new_products['results']

    products_sorted = sorted(
                    products['results'],
                    key = lambda i: i[order_by],
                    reverse=True)

    return products_sorted


# Create your views here.

class HomeView(TemplateView):
    """
        Pagina principal
    """

    template_name = 'listing/home.html'

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        api_authenticated = Application.get_authorized(user=current_user)

        if api_authenticated:
            meli = Meli(
                    client_id=api_authenticated.app_id,
                    client_secret=api_authenticated.secret_key,
                    access_token=api_authenticated.access_token,
                    refresh_token=api_authenticated.refresh_token
                    )

            access_token = meli.get_refresh_token()
            api_authenticated.refresh_token = meli.refresh_token
            api_authenticated.save()

            if access_token:
                user = meli.get(
                        '/users/me?access_token={}'
                        .format(access_token))
        
        form = SelectAppForm()
        form.fields['application'].queryset = Application.objects.filter(user=current_user)

        
        return {
            'form': form,
            'authenticated': api_authenticated,
            'user': current_user,
            'user_api': user
            }


class ListingsView(TemplateView):
    """
        Pagina donde podremos seleccionar
        el listado que querramos visualizar.
    """

    template_name = 'listing/listings.html'
    def get_context_data(self, *args, **kwargs):
            application_id = self.request.GET.get('application')
            data = Application.get_by_id(int(application_id))

            meli = Meli(
                    client_id=data.app_id,
                    client_secret=data.secret_key,
                    access_token=data.access_token,
                    refresh_token=data.refresh_token
                    )

            access_token = meli.get_refresh_token()
            data.refresh_token = meli.refresh_token
            data.save()

            if (access_token):
                user = meli.get(
                        '/users/me?access_token={}'
                        .format(access_token))

                return {
                    'user_info': user,
                    'Error': '',
                    'application': application_id
                    }
            else:
                return {
                    'Error': 'No se pudo obtener el Token'
                    }


class ListingTopSeller(TemplateView):
    """
        Listado de los iphone mas vendidos
        ordenados y mostrando los primeros 10.
    """

    template_name = 'listing/sold_quantity.html'

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user

        app_authenticated = Application.get_authorized(current_user)

        meli = Meli(
                client_id=app_authenticated.app_id,
                client_secret=app_authenticated.secret_key,
                access_token=app_authenticated.access_token,
                refresh_token=app_authenticated.refresh_token
                )

        access_token = meli.get_refresh_token()
        app_authenticated.refresh_token = meli.refresh_token
        app_authenticated.save()

        if (access_token):
            user = meli.get(
                    '/users/me?access_token={}'
                    .format(access_token))

            user_info = json.loads(user.text)

            products_sorted = top_product_list('sold_quantity', meli, access_token)

            for product in products_sorted[:10]:
                user_id = product['seller']['id']
                user = meli.get('/users/{}'.format(user_id))
                user_json = json.loads(user.text)
                product['seller'].update({'nickname': user_json['nickname']})

            return {
                'products': products_sorted[:10],
                'user_info': user_info, 
                'Error': '',
                'application': app_authenticated.id
                }
            
        else:
            return { 'Error': 'No se pudo obtener el Token' }


class ListingHigherPrice(TemplateView):
    """
        Listado de la categoria ordenados por mayor precio
        mostrando solo los 10 mas caros.
    """
    
    template_name = 'listing/higher_price.html'

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user

        app_authenticated = Application.get_authorized(current_user)

        meli = Meli(
                client_id=app_authenticated.app_id,
                client_secret=app_authenticated.secret_key,
                access_token=app_authenticated.access_token,
                refresh_token=app_authenticated.refresh_token
                )

        access_token = meli.get_refresh_token()

        if (access_token):
            user = meli.get(
                    '/users/me?access_token={}'
                    .format(access_token))

            user_info = json.loads(user.text)

            products_sorted = top_product_list(
                                'price',
                                meli,
                                access_token)

            return {
                'products': products_sorted[:10],
                'user_info': user_info,
                'Error': '',
                'application': app_authenticated.id
                }
        else:
            return {'Error': 'Falta token'}
