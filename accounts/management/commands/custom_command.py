from typing import Any
from django.core.management.base import BaseCommand
from accounts.models import RequestCount


class Command(BaseCommand):
    help = ""

    def handle(self, *args: Any, **options: Any) -> str | None:
        count, created = RequestCount.objects.get_or_create(
                                id=1, defaults={'count': 0})
        if not created:
            count.count = 0
            count.save()
        print(self.style.HTTP_SUCCESS("Counter reseted succesfully!"))
        print("dsnfsgnsgnsfghs")
