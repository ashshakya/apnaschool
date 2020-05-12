import sys

from django.contrib import admin

from django.contrib.admin.filters import (
    SimpleListFilter,
    AllValuesFieldListFilter,
    ChoicesFieldListFilter,
    RelatedFieldListFilter,
    RelatedOnlyFieldListFilter
)


class SimpleDropdownFilter(SimpleListFilter):
    template = 'admin/dropdown_filter.html'


class DropdownFilter(AllValuesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class ChoiceDropdownFilter(ChoicesFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedDropdownFilter(RelatedFieldListFilter):
    template = 'admin/dropdown_filter.html'


class RelatedOnlyDropdownFilter(RelatedOnlyFieldListFilter):
    template = 'admin/dropdown_filter.html'


def try_or(fn, default):
    """
    Jugaad for a one liner try:except block.
    Usage: try_or(lambda: request_user.email, None)
    """
    try:
        return fn()
    except Exception:
        return default


def import_class(path):
    """
    Imports a class based on a full Python path ('pkg.pkg.mod.Class'). This
    does not trap any exceptions if the path is not valid.
    """
    module, name = path.rsplit('.', 1)
    __import__(module)
    mod = sys.modules[module]
    cls = getattr(mod, name)

    return cls


class InputFilter(admin.SimpleListFilter):
    template = 'admin/input_filter.html'

    def lookups(self, request, model_admin):
        # Dummy, required to show the filter.
        return ((),)

    def choices(self, changelist):
        # Grab only the 'all' option.
        all_choice = next(super().choices(changelist))
        all_choice['query_parts'] = (
            (k, v)
            for k, v in changelist.get_filters_params().items()
            if k != self.parameter_name
        )
        yield all_choice
