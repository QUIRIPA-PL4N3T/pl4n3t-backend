from django.core.management.base import BaseCommand

from emissions.models import GreenhouseGas, EmissionFactor, GreenhouseGasEmission
from main.models import UnitOfMeasure


class Command(BaseCommand):
    help = 'Crea emisiones de gases de efecto invernadero por defecto para cada factor de emisión'

    def handle(self, *args, **kwargs):
        default_unit, _ = UnitOfMeasure.objects.get_or_create(name='kg')
        gases = GreenhouseGas.objects.all()

        for factor in EmissionFactor.objects.all():
            for gas in gases:
                _, created = GreenhouseGasEmission.objects.get_or_create(
                    emission_factor=factor,
                    greenhouse_gas=gas,
                    defaults={
                        'unit': default_unit,
                        'value': 0.0,
                        'percentage_uncertainty': 0.0,
                        'maximum_allowed_amount': 0.0
                    }
                )
                if created:
                    self.stdout.write(f'Emisión por defecto creada para factor: {factor.name}, gas: {gas.name}')

        self.stdout.write(self.style.SUCCESS('Emisiones por defecto creadas exitosamente.'))
