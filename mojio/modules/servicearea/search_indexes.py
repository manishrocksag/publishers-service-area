from haystack import indexes
from .models import ServiceArea


class ServiceAreaIndex(indexes.SearchIndex, indexes.Indexable):
        text = indexes.CharField(document=True, use_template=True, template_name="search/book_text.txt")
        coordinate = indexes.CharField(model_attr='title')
        publisher = indexes.CharField()

        def get_model(self):
            return ServiceArea

        def prepare_service_area(self, obj):
            return [coordinate for coordinate in obj.coordinates.all()]

        def index_queryset(self, using=None):
            return self.get_model().objects.all()