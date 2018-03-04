from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import TemplateView
from apps.applicationML.sdk.lib.meli import Meli
from apps.applicationML.forms import SelectAppForm
from .models import Application


# Create your views here.

class HomeApplicationView(TemplateView):
    template_name = 'applicationML/home.html'

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        user_authenticated = Application.get_authorized(current_user)
        if not user_authenticated:

            form = SelectAppForm()
            form.fields['application'].queryset = Application.objects.filter(user=current_user)

            return {
                'form': form,
                'user': current_user
                }
        else:
            return {
                'authenticated': user_authenticated
                }


class AuthorizingView(TemplateView):
    def get(self, request):
        application_id = self.request.GET.get('application')
        data = Application.get_by_id(int(application_id))
        current_user = self.request.user

        user_authenticated = Application.get_authorized(current_user)

        if user_authenticated:
            user_authenticated.authorized = False
            user_authenticated.save()

        data.authorized = True
        data.save()

        meli = Meli(
                client_id=data.app_id,
                client_secret=data.secret_key)

        return redirect(meli.auth_url(redirect_URI='http://localhost:8080/authorized'))


class AuthorizedView(TemplateView):
    template_name = 'applicationML/authorized.html'

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        app_authenticated = Application.get_authorized(current_user)

        meli = Meli(
            client_id=app_authenticated.app_id,
            client_secret=app_authenticated.secret_key)

        code = self.request.GET.get('code')

        if (code):
            try:
                meli.authorize(code, 'http://localhost:8080/authorized')
                app_authenticated.refresh_token = meli.refresh_token
                app_authenticated.access_token = meli.access_token
                app_authenticated.save()
                message = 'El usuario se autentico con exito'
                error = ''
            except:
                app_authenticated.authorized = False
                app_authenticated.save()
                error = 'Error al autenticar'
                message = error

                return {
                    'user': {},
                    'Error': 'No esta autenticado'
                    }

            return {
                'user': current_user,
                'message':message,
                'app': app_authenticated
                }

        else:
            return {'Error': 'No existe token'}



class LogoutML(TemplateView):
    def get(self, request):
        return redirect('https://www.mercadolibre.com/jms/mla/lgz/logout?go=localhost:8080')