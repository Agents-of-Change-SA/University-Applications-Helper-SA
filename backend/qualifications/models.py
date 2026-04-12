from django.db import models


class Institution(models.Model):
    """A South African university or college."""
    name = models.CharField(max_length=255, unique=True)
    abbreviation = models.CharField(max_length=20, blank=True, default='')

    class Meta:
        ordering = ['name']
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'

    def __str__(self):
        return self.abbreviation or self.name


class Qualification(models.Model):
    """A tertiary qualification offered by an institution."""
    institution = models.ForeignKey(
        Institution,
        on_delete=models.CASCADE,
        related_name='qualifications',
    )
    slug = models.SlugField(max_length=100, unique=True)
    name = models.CharField(max_length=255)
    qualification_code = models.CharField(max_length=50, blank=True, default='')
    faculty = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(blank=True, default='')
    minimum_aps = models.PositiveIntegerField()

    class Meta:
        ordering = ['institution', 'name']
        verbose_name = 'Qualification'
        verbose_name_plural = 'Qualifications'

    def __str__(self):
        return f"{self.name} ({self.institution})"


class APSRule(models.Model):
    """
    Subject-dependent minimum APS rule.
    e.g. "25 with Mathematics level 4, OR 26 with Mathematical Literacy level 5"
    """
    RULE_TYPES = [
        ('subject_dependent_minimum_aps', 'Subject-dependent minimum APS'),
    ]

    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        related_name='aps_rules',
    )
    rule_type = models.CharField(max_length=50, choices=RULE_TYPES)

    class Meta:
        ordering = ['pk']
        verbose_name = 'APS Rule'
        verbose_name_plural = 'APS Rules'

    def __str__(self):
        return f"{self.rule_type} for {self.qualification}"


class APSRuleCondition(models.Model):
    """A single condition within an APS rule."""
    rule = models.ForeignKey(
        APSRule,
        on_delete=models.CASCADE,
        related_name='conditions',
    )
    subject = models.CharField(max_length=100)
    minimum_level = models.PositiveIntegerField()
    min_aps = models.PositiveIntegerField()

    class Meta:
        ordering = ['pk']
        verbose_name = 'APS Rule Condition'
        verbose_name_plural = 'APS Rule Conditions'

    def __str__(self):
        return f"{self.subject} level {self.minimum_level} → APS {self.min_aps}"


class SubjectRequirement(models.Model):
    """A subject requirement for a qualification."""
    REQUIREMENT_TYPES = [
        ('mandatory', 'Mandatory'),
        ('one_of', 'One of (alternative)'),
        ('disallowed', 'Disallowed'),
    ]

    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        related_name='subject_requirements',
    )
    requirement_type = models.CharField(max_length=20, choices=REQUIREMENT_TYPES)
    subject = models.CharField(max_length=100)
    minimum_level = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['requirement_type', 'subject']
        verbose_name = 'Subject Requirement'
        verbose_name_plural = 'Subject Requirements'

    def __str__(self):
        return f"{self.requirement_type}: {self.subject} (level {self.minimum_level})"


class SelectionRequirement(models.Model):
    """Additional selection criteria (e.g. portfolio, interview)."""
    SELECTION_TYPES = [
        ('possible_portfolio', 'Possible Portfolio'),
        ('required_portfolio', 'Required Portfolio'),
        ('interview', 'Interview'),
        ('nbt', 'NBT'),
        ('other', 'Other'),
    ]

    qualification = models.ForeignKey(
        Qualification,
        on_delete=models.CASCADE,
        related_name='selection_requirements',
    )
    selection_type = models.CharField(max_length=30, choices=SELECTION_TYPES)
    required = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['pk']
        verbose_name = 'Selection Requirement'
        verbose_name_plural = 'Selection Requirements'

    def __str__(self):
        return f"{self.selection_type} ({'required' if self.required else 'optional'})"
