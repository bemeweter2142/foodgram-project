from django.contrib.auth import get_user_model

User = get_user_model()

# Если есть, выводятся ФИ, иначе логин
def get_user_name(self):
    if self.first_name or self.last_name:
        return f'{self.first_name} {self.last_name}'
    return self.username





User.add_to_class('__str__', get_user_name)