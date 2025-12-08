import json
from pathlib import Path
from django.core.management.base import BaseCommand
from app_allergens.models import Allergen, AllergenKeyword

class Command(BaseCommand):
    help = "Seeds allergens and keywords into database"

    def handle(self, *args, **kwargs):
        file_path = Path("app_allergens/data/allergens.json")

        if not file_path.exists():
            self.stdout.write(self.style.ERROR("allergens.json not found"))
            return

        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        for item in data:
            allergen, created = Allergen.objects.get_or_create(
                name=item["name"],
                category=item.get("category", "allergy"),
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f"Created allergen: {allergen.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Exists: {allergen.name}"))

            keywords = item.get("keywords", [])
            for word in keywords:
                AllergenKeyword.objects.get_or_create(
                    allergen=allergen,
                    keyword=word.lower().strip()
                )

        self.stdout.write(self.style.SUCCESS("Allergens seeded successfully"))
