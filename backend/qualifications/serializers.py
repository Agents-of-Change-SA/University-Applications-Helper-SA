from rest_framework import serializers

from .models import (
    APSRule,
    APSRuleCondition,
    Institution,
    Qualification,
    SelectionRequirement,
    SubjectRequirement,
)


# ── Nested read serializers ──

class APSRuleConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = APSRuleCondition
        fields = ['subject', 'minimum_level', 'min_aps']


class APSRuleSerializer(serializers.ModelSerializer):
    conditions = APSRuleConditionSerializer(many=True, read_only=True)

    class Meta:
        model = APSRule
        fields = ['id', 'rule_type', 'conditions']


class SubjectRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubjectRequirement
        fields = ['subject', 'minimum_level']


class SelectionRequirementSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='selection_type')

    class Meta:
        model = SelectionRequirement
        fields = ['type', 'required', 'notes']


class SubjectRequirementsGroupSerializer(serializers.Serializer):
    """Groups subject requirements by type: mandatory, one_of, disallowed."""
    mandatory = SubjectRequirementSerializer(many=True)
    one_of = SubjectRequirementSerializer(many=True)
    disallowed = SubjectRequirementSerializer(many=True)


class QualificationSerializer(serializers.ModelSerializer):
    aps_rules = APSRuleSerializer(many=True, read_only=True)
    subject_requirements = serializers.SerializerMethodField()
    selection_requirements = SelectionRequirementSerializer(many=True, read_only=True)

    class Meta:
        model = Qualification
        fields = [
            'id', 'slug', 'name', 'qualification_code', 'faculty',
            'description', 'minimum_aps', 'aps_rules',
            'subject_requirements', 'selection_requirements',
        ]

    def get_subject_requirements(self, obj):
        reqs = obj.subject_requirements.all()
        return {
            'mandatory': SubjectRequirementSerializer(
                reqs.filter(requirement_type='mandatory'), many=True,
            ).data,
            'one_of': SubjectRequirementSerializer(
                reqs.filter(requirement_type='one_of'), many=True,
            ).data,
            'disallowed': SubjectRequirementSerializer(
                reqs.filter(requirement_type='disallowed'), many=True,
            ).data,
        }


class QualificationListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views."""
    institution_name = serializers.CharField(source='institution.name', read_only=True)
    institution_abbr = serializers.CharField(source='institution.abbreviation', read_only=True)

    class Meta:
        model = Qualification
        fields = [
            'id', 'slug', 'name', 'qualification_code', 'faculty',
            'minimum_aps', 'institution_name', 'institution_abbr',
        ]


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        fields = ['id', 'name', 'abbreviation']


class InstitutionDetailSerializer(serializers.ModelSerializer):
    qualifications = QualificationListSerializer(many=True, read_only=True)

    class Meta:
        model = Institution
        fields = ['id', 'name', 'abbreviation', 'qualifications']
