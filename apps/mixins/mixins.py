from rest_framework.viewsets import mixins
from rest_framework.viewsets import GenericViewSet


class RetrivListViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pass


class CreateGetListViewSet(GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    pass


class WithoutDeleteViewSet(CreateGetListViewSet, mixins.UpdateModelMixin):
    pass
