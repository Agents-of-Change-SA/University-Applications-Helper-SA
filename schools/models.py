from pathlib import Path
from django.db import models
from django.core.exceptions import ValidationError
import csv

# Create your models here.
# Helper to load CSV choices
def load_choices(filename):
    choices_path = Path(__file__).resolve().parent / "choices" / filename
    with open(choices_path, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        return [(row[0], row[1]) for row in reader]


class Institution(models.Model):
    """Allows for a choice of Institution.
    
    Institutions are presented in three forms following the actual representation in the country.
    These are - University, University of Technology and TVET Colleges. 
    A choice is made for each Institution at instantiation.
    """
    type_choices = [
        ('UNI', 'University'),
        ('UoTech', 'University of Technology'),
        ('TVET', 'TVET College')
    ]

    name = models.CharField(max_length=200)
    type = models.CharField(max_length=100, choices=type_choices)

    def __str__(self):
        return f'''
            {self.name}\n
            {self.type}
        '''

class Faculty(models.Model):
    '''
    The Faculty model represents the name of a faculty of an institution.
    Any two or more institutions can have the same faculty. Hence the ManyToManyField().
    '''
    name = models.CharField(max_length=100)
    institution = models.ManyToManyField(Institution, through="Course")


    def __str__(self):
        return f'{self.name}'

class School(models.Model):    
    '''
    The School model has the name of the school, the schools abbreviation and the ManyToManyField named for faculty.
    This anticipates that a scho
    '''
    name = models.CharField(max_length=200, blank=True, null=True)
    abbreviation = models.CharField(max_length=50, blank=True, null=True)
    faculty = models.ManyToManyField(Faculty, through="Course")    
    def __str__(self):
        return f'{self.name} - {self.abbreviation}'


class SubjectChoices(models.Model):
    SymbolChoices = [(code, int(value)) for code, value in load_choices("symbol_choices.csv")]

    Selectives = load_choices("selectives.csv")

    SubjectLevels = load_choices("subject_levels.csv")

    name = models.CharField(max_length=200, choices=[(choice[1], choice[1]) for choice in Selectives])
    level = models.IntegerField(choices=[(choice[1], choice[1]) for choice in SymbolChoices], default=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
    def clean(self):
        if self.level not in self.SubjectLevels.get(self.name, []):
            raise ValidationError('Invalid level for the chosen subject')

    def __str__(self):
        return f'{self.name, self.level}'


class Course(models.Model):    
    """The Course model is about the courses of an institution.
    
    The Model keeps data about the courses and their requirements. 
    """
    name = models.CharField(max_length=200)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    School = models.ForeignKey(School, on_delete=models.CASCADE, blank=True, null=True)
    Subjects = models.ManyToManyField(SubjectChoices)
    APS = models.IntegerField(default=0)
    Duration = models.IntegerField(default=0)
    NBT = models.BooleanField(default=False)
    Requirements = models.TextField(max_length=1000, null=True, blank=True)
    
    def __str__(self):
        return f'{self.name}'
    



    
    
