# from rest_framework.generics import GenericAPIView
# from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin
# from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin
# from rest_framework.permissions import IsAuthenticated
# from ..serializers import DealSerializer
# from deals.models import Deal
# from ..serializers import Deal_Serializer

# class DealListCreateView(GenericAPIView, ListModelMixin, CreateModelMixin):
#     queryset = Deal.objects.filter(is_approved=True).order_by('-created_at')
#     serializer_class = DealSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)

# class DealDetailView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
#     queryset = Deal.objects.all()
#     serializer_class = DealSerializer
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

