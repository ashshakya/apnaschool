from rest_framework import serializers

from apnaschool.data.models import FeeStructure


class FeeStructureSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeeStructure
        fields = ('fee')
        read_only_fields = ('standard')
