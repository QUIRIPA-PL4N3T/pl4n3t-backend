from django.core.management.base import BaseCommand
from emission_source_classifications.models import CommonEquipment, EmissionSourceGroup


class Command(BaseCommand):
    help = 'Load sample CommonEquipment data into the database'

    def handle(self, *args, **kwargs):
        # Get the EmissionSourceGroup with id 7
        try:
            group = EmissionSourceGroup.objects.get(id=7)
        except EmissionSourceGroup.DoesNotExist:
            self.stdout.write(self.style.ERROR('EmissionSourceGroup with id 7 does not exist'))
            return

        equipment_list = [
            "Chiller de absorción",
            "Unidad de tratamiento de aire (UTA)",
            "Enfriador de agua",
            "Condensador evaporativo",
            "Refrigerador industrial",
            "Congelador industrial",
            "Compresor de refrigeración",
            "Torre de enfriamiento",
            "Evaporador",
            "Unidad de refrigeración en contenedores",
            "Sistema de refrigeración en supermercados",
            "Unidad de refrigeración de transporte",
            "Enfriador de proceso",
            "Sistema de refrigeración criogénica",
            "Enfriador de aceite",
            "Unidad de refrigeración de laboratorio",
            "Enfriador de gas",
            "Refrigerador de líquidos industriales",
            "Sistema de refrigeración en barcos",
            "Unidad de refrigeración portátil"
        ]

        for equipment_name in equipment_list:
            CommonEquipment.objects.get_or_create(
                name=equipment_name,
                group=group
            )

        self.stdout.write(self.style.SUCCESS('Successfully loaded sample CommonEquipment data'))
