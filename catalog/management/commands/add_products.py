from django.core.management.base import BaseCommand
from django.core.management import call_command
from catalog.models import Category, Product


class Command(BaseCommand):
    help = 'Полностью очищает и наполняет базу данными из фикстуры catalog_fixture'

    def handle(self, *args, **options):
        self.stdout.write("Удаление всех существующих данных...")

        # 1. Очищаем базу данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Данные успешно удалены."))

        # 2. Загружаем данные из файла фикстуры
        self.stdout.write("Загрузка данных из фикстуры...")
        call_command('loaddata', 'catalog_fixture', app_label='catalog', verbosity=0)
        self.stdout.write(self.style.SUCCESS("База данных успешно наполнена из фикстуры!"))
