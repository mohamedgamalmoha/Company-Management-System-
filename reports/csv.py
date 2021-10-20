import csv
from typing import List

from django.db.models import Model, QuerySet
from django.core.exceptions import ImproperlyConfigured
from django.views.generic.base import View, ContextMixin

from django.http import HttpResponse
from django.http.response import HttpResponseBase


class BaseView(ContextMixin, View):
    response_class: HttpResponseBase = HttpResponse
    content_type: str

    def get(self, request, *args, **kwargs):
        """Get method initialization"""
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)

    def render_to_response(self, context, **response_kwargs) -> HttpResponseBase:
        """Response content data"""
        response_kwargs.setdefault('content_type', self.content_type)
        return self.response_class(request=self.request, context=context, **response_kwargs)


class ModelCSVResponse(BaseView):

    model: Model
    csv_queryset: QuerySet = None
    csv_ordering: str = None

    csv_columns: List[str] = []
    csv_extra_columns: List[str] = []
    csv_fields: List[str] = []
    csv_exclude_fields: List[str] = []
    csv_extra_fields: List[str] = []

    csv_file_name: str = None
    content_type: str = 'text/csv'

    def init(self, model, **kwargs):
        """Custom initialization for new instance."""
        if not model:
            raise ValueError('model must be entered')
        self.model = model
        for key, val in kwargs.items():
            if hasattr(self, key) and val:
                setattr(self, key, val)

    def get_csv_model_fields_names(self) -> List[str]:
        """Return model field or fields without excluded ones."""
        fields = self.csv_fields or map(lambda field: field.name, self.model._meta.fields)
        fields.extend(self.csv_extra_fields)
        lst_fields = filter(lambda field_name: field_name not in self.csv_exclude_fields, fields)
        return list(lst_fields)

    def get_csv_queryset(self, queryset=None) -> QuerySet:
        """Return ordering queryset - in case csv_ordering is specified - to use for writing csv file."""
        queryset = queryset or self.csv_queryset or self.model._default_manager.all()

        if queryset is None:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.csv_queryset, or override "
                "%(cls)s.get_csv_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )

        ordering = self.get_csv_ordering()
        if ordering:
            if isinstance(ordering, str):
                ordering = (ordering, )
            queryset = queryset.order_by(*ordering)

        return queryset

    def get_csv_columns(self) -> List[str]:
        """Return csv columns."""
        lst = self.csv_columns or self.get_csv_model_fields_names()
        lst.extend(self.csv_extra_columns)
        return lst

    def get_csv_model_fields(self, obj) -> List[str]:
        return [value() if callable(value := getattr(obj, field)) else value for field in
                self.get_csv_model_fields_names()]

    def get_csv_rows(self) -> List[List[str]]:
        """Return csv rows."""
        return [self.get_csv_model_fields(obj) for obj in self.get_csv_queryset().all()]

    def get_csv_file_name(self) -> str:
        """Return csv filename."""
        return self.csv_file_name or self.model._meta.model_name

    def get_csv_ordering(self) -> str:
        """Return the field or fields to use for ordering the queryset."""
        return self.csv_ordering

    def handle_response(self, **response_kwargs):
        """It handles the response in case if it needs to be updated."""
        response_kwargs.setdefault('content_type', self.content_type)
        response = self.response_class(**response_kwargs)
        response['Content-Disposition'] = f'attachment; filename="{self.get_csv_file_name()}.csv"'
        return response

    @staticmethod
    def write_csv(response, headers, rows):
        """It handles the writing of csv file."""
        writer = csv.writer(response)
        writer.writerow(headers)
        for row in rows:
            writer.writerow(row)
        return response

    def render_to_response(self, context: dict = None, **response_kwargs):
        """Return csv file response."""
        rows = self.get_csv_rows()
        columns = self.get_csv_columns()
        response = self.handle_response(**response_kwargs)
        return self.write_csv(response, columns, rows)


class BaseRelationalModelCSVResponse(ModelCSVResponse):
    csv_model_related_field_name: str = None
    csv_model_related_fields: List[str] = None

    def get_csv_default_related_fields_names(self) -> List[str]:
        """Get all default related fields for model instance."""
        return [obj.name for obj in self.model._meta.related_objects]

    def get_csv_related_field_queryset(self, obj: Model) -> QuerySet:
        """Get all relational objects."""
        if self.csv_model_related_field_name not in self.get_csv_default_related_fields_names():
            raise ValueError('invalid')
        queryset = getattr(obj, self.csv_model_related_field_name)
        return queryset.all()

    def get_csv_model_related_fields(self) -> List[str]:
        """Get model related fields required list"""
        return self.csv_model_related_fields

    def get_csv_related_fields(self, obj: Model) -> List[str]:
        """Get model related fields required list values"""
        raise NotImplemented

    def get_csv_columns(self) -> List[str]:
        """Add related fields to columns."""
        columns = super().get_csv_columns()
        columns.extend(self.csv_model_related_fields)
        return columns

    def get_csv_rows(self) -> List[List[str]]:
        """Return csv rows."""
        raise NotImplemented


class SingleRelationalModelCSVResponse(BaseRelationalModelCSVResponse):

    def get_csv_related_fields(self, obj: Model) -> List[str]:
        """Get model related fields required list values"""
        related_object = self.get_csv_related_field_queryset(obj).last()
        if related_object is not None:
            return [value() if callable(value := getattr(related_object, related_field)) else value for related_field
                    in self.get_csv_model_related_fields()]
        return []

    def get_csv_rows(self) -> List[List[str]]:
        """Return csv rows."""
        rows_lst = []
        obj = self.get_csv_queryset()
        if isinstance(obj, QuerySet):
            obj = obj.last()

        # Get model fields for each instance
        row_lst = self.get_csv_model_fields(obj)

        # Get model related fields for each instance
        related_objects = self.get_csv_related_field_queryset(obj).all()
        for related_object in related_objects:
            related_objects_lst = row_lst[:]
            if related_object is not None:
                related_objects_lst.extend([value() if callable(value := getattr(related_object, related_field))
                                            else value for related_field in self.get_csv_model_related_fields()])
            rows_lst.append(related_objects_lst)

        return rows_lst


class MultiRelationalModelCSVResponse(BaseRelationalModelCSVResponse):

    def get_csv_related_fields(self, obj: Model) -> List[str]:
        """Get model related fields required list values"""
        related_object = self.get_csv_related_field_queryset(obj).last()
        if related_object is not None:
            return [value() if callable(value := getattr(related_object, related_field)) else value for related_field
                    in self.get_csv_model_related_fields()]
        return []

    def get_csv_rows(self) -> List[List[str]]:
        """Return csv rows."""
        rows_lst = []
        for obj in self.get_csv_queryset().all():

            # Get model fields for each instance
            row_lst = self.get_csv_model_fields(obj)

            # Get model related fields for each instance
            row_lst.extend(self.get_csv_related_fields(obj))

            # Append to rows list
            rows_lst.append(row_lst)

        return rows_lst


class NewVersionSingleRelationalModelCSVResponse(SingleRelationalModelCSVResponse):
    after_csv_fields: list = None

    def get_csv_rows(self):
        """Return csv rows."""
        rows_lst = []
        obj = self.get_csv_queryset()

        # Get model fields for each instance
        row_lst = self.get_csv_model_fields(obj)

        # Get model related fields for each instance
        related_objects = self.get_csv_related_field_queryset(obj).all()
        for related_object in related_objects:
            related_objects_lst = row_lst[:]
            if related_object is not None:
                related_objects_lst.extend([value() if callable(value := getattr(related_object, related_field))
                                            else value for related_field in self.get_csv_model_related_fields()])
            rows_lst.append(related_objects_lst)

        after_csv_fields = [(field, value()) if callable(value := getattr(obj, field)) else (field, value) for field
                            in self.after_csv_fields]
        rows_lst.extend(after_csv_fields)
        return rows_lst


def cls_to_func_csv_action(model: Model, csv_class: ModelCSVResponse = ModelCSVResponse, **kwargs):
    """Turn CSV class to function to be used more than once"""
    response = csv_class()
    response.init(model, **kwargs)
    return response.render_to_response()
