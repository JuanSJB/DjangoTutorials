from django.core.management.base import BaseCommand
from pages.factories import ProductFactory  # Asegúrate de que el import es correcto

class Command(BaseCommand):
    help = 'Crea productos de prueba usando factory_boy'

    def handle(self, *args, **kwargs):
        for _ in range(10):
            producto = ProductFactory()
            self.stdout.write(self.style.SUCCESS(f'Producto creado: {producto.name} - ${producto.price}'))
