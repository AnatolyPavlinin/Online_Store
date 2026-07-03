from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Group, Permission
from catalog.models import Product

class Command(BaseCommand):
    help = 'Creates moderator group with can_unpublish_product permission'

    def handle(self, *args, **options):
        product_ct = ContentType.objects.get_for_model(Product)
        perm, created = Permission.objects.get_or_create(
            codename='can_unpublish_product',
            name='Может снимать с публикации',
            content_type=product_ct
        )

        moderators, created = Group.objects.get_or_create(name='Модераторы продуктов')

        moderators.permissions.add(
            perm,
            Permission.objects.get(codename='delete_product')
        )

        self.stdout.write(self.style.SUCCESS('Группа "Модераторы" создана'))