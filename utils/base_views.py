from rest_framework import generics


class BaseGenericAPIView(generics.GenericAPIView):
    http_method_names = ["get", "post", "patch", "delete", "head", "options", "head", "put"]

    class Meta:
        abstract = True