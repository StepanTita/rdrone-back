from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from django.db.models import Sum

from occasions.models import Occasion, Comment, Resolutions
from occasions.serializers import OccasionSerializer, CommentSerializer, ResolutionsResponseSerializer, \
    ResolutionsSerializer


class OccasionsListCreateView(generics.ListCreateAPIView):
    queryset = Occasion.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OccasionSerializer


class OccasionsRetrieveView(generics.RetrieveUpdateAPIView):
    queryset = Occasion.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = OccasionSerializer


class CommentsCreateListView(generics.CreateAPIView, generics.ListAPIView):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def create(self, request, *args, **kwargs):
        request.data['occasion_id'] = kwargs['pk']
        request.data['user_id'] = request.user.id
        return super(CommentsCreateListView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        occasion = self.kwargs['pk']
        return Comment.objects.filter(occasion=occasion)


class ResolutionsResponseView(generics.GenericAPIView):
    queryset = Resolutions.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ResolutionsResponseSerializer

    def to_int(self, val):
        return 0 if val is None else int(val)

    def get(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        count_rejected = self.to_int(queryset.aggregate(Sum('rejected'))['rejected__sum'])
        count_resolved = self.to_int(queryset.aggregate(Sum('resolved'))['resolved__sum'])

        try:
            resolution = queryset.get(
                user=request.user.id
            )
        except Resolutions.DoesNotExist:
            resolution = None

        option = ''
        if resolution is not None:
            if resolution.rejected == 1:
                option = 'rejected'
            elif resolution.resolved == 1:
                option = 'resolved'
        print(count_rejected)
        serializer = self.get_serializer({
            'rejected': count_rejected,
            'resolved': count_resolved,
            'option': option
        })
        return Response(serializer.data)

    def get_queryset(self):
        occasion = self.kwargs['pk']
        return Resolutions.objects.filter(occasion=occasion)


class ResolutionsView(generics.CreateAPIView):
    queryset = Resolutions.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = ResolutionsSerializer

    def create(self, request, *args, **kwargs):
        # todo make decorator
        request.data['occasion_id'] = kwargs['pk']
        request.data['user_id'] = request.user.id
        option = self.kwargs['option']
        if option == 'resolved':
            request.data['resolved'] = 1
        else:
            request.data['rejected'] = 1

        res = super(ResolutionsView, self).create(request, *args, **kwargs)

        occasion = Occasion.objects.get(id=self.kwargs['pk'])
        option = self.kwargs['option']
        if option == 'resolved':
            occasion.resolved += 1
            request.data['resolved'] = 1
        else:
            occasion.rejected += 1
            request.data['rejected'] = 1
        occasion.save()

        return res
