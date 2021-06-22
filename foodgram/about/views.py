from django.views.generic.base import TemplateView


class AboutAuthorView(TemplateView):
    template_name = 'about/about_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Об авторе'
        context['text'] = 'Интересные факты об авторе: (отсутствуют)'
        return context


class AboutTechView(TemplateView):
    template_name = 'about/about_template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Технологии'
        context['text'] = ('Проект продуктового помощника написан '
                           'на Python с помощью фреймворков '
                           'Django и Django REST')
        return context
