import random
from webbrowser import get
from django.core.management.base import BaseCommand
from itp.models import Publication, Conference, Tag
from django.contrib.auth.models import User


fields = ('author', 'type', 'year', 'magazine', 'page','doi', 'conferenceid', 'tag' )

type = [
    'Journal',
    'Conference',
    'Technical Reports',
]

magazine = [
    'Database Trends and Applications',
    'ODBMS',
    'PubMed Central',
    'ResearchGate',
    'HAL',
    'RePEc: Research Papers in Economics',
    'Academic Search',
    'AGRIS: Agricultural database',
    'Foundations and Trends® in Machine Learning',
    'Journal of Big Data',
]

def generate_type_name():
    index = random.randint(0, 2)
    return type[index]

def generate_magazine_name():
    index = random.randint(0, 9)
    return magazine[index]



class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'file_name', type=str, help='The txt file that contains the journal titles.')

    def handle(self, *args, **kwargs):
        file_name = kwargs['file_name']
        with open(f'{file_name}.txt') as file:
            for row in file:
                title = row
                author_id = random.randint(1, 11)
                type = generate_type_name()
                year = random.randint(1990, 2022)
                magazine = generate_magazine_name()
                page = random.randint(1, 600)
                doi = random.randint(1010000, 1019999)
                conferenceid = random.randint(1, 3)
                tagid = random.randint(1, 7)

                publication = Publication(
                    title=title,
                    type = type,
                    year = year,
                    magazine = magazine,
                    page = page,
                    conferenceid=Conference.objects.get(id=conferenceid),
                    doi = doi
                    )

                publication.save()

                publication.author.add(User.objects.get(id=author_id))
                publication.tag.add(Tag.objects.get(id=tagid))

                print(title, author_id, type, year, magazine, page, doi, conferenceid, tagid)
                

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))