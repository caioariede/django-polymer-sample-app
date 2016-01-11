import datetime

from django.db.models import Avg, Sum

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

from .models import Track
from .serializers import TrackSerializer


class TrackList(generics.ListCreateAPIView):
    queryset = Track.objects.order_by('-pk')
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def filter_queryset(self, qs):
        qs = qs.filter(user=self.request.user)

        dateFrom = self.request.GET.get('dateFrom')
        dateTo = self.request.GET.get('dateTo')

        if dateFrom and dateTo:
            qs = qs.filter(date__range=(dateFrom, dateTo))

        return qs


class TrackDestroy(generics.DestroyAPIView):
    queryset = Track.objects.order_by('-pk')
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, qs):
        return qs.filter(user=self.request.user)


class TrackUpdate(generics.UpdateAPIView):
    queryset = Track.objects.order_by('-pk')
    serializer_class = TrackSerializer
    permission_classes = (IsAuthenticated,)

    def filter_queryset(self, qs):
        return qs.filter(user=self.request.user)


class WeeklyReport(APIView):
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        dateFrom = self.request.GET.get('dateFrom')
        dateTo = self.request.GET.get('dateTo')

        if not dateFrom or not dateTo:
            return Response([])

        try:
            dateFrom = datetime.datetime.strptime(dateFrom, '%Y-%m-%d')
            dateTo = datetime.datetime.strptime(dateTo, '%Y-%m-%d')
        except ValueError:
            return Response([])

        # move to start of the week / end of the week
        dateFrom -= datetime.timedelta(days=dateFrom.weekday())
        dateTo += datetime.timedelta(days=(6 - dateTo.weekday()))

        result = []

        while dateFrom < dateTo:
            nextWeek = dateFrom + datetime.timedelta(days=7)

            tracks = Track.objects.filter(
                date__gte=dateFrom, date__lt=nextWeek, user=self.request.user)

            a = tracks.aggregate(
                Avg('distance'), Sum('distance'), Sum('time'))

            if a['time__sum']:
                dist = a['distance__sum'] * 1000
                secs = a['time__sum'].total_seconds()
                avg_speed = round((dist / secs) * 3.6, 2)

                result.append({
                    'date_start': dateFrom,
                    'date_end': nextWeek - datetime.timedelta(days=1),
                    'avg_distance': a['distance__avg'],
                    'avg_speed': avg_speed,
                })

            dateFrom = nextWeek

        return Response(reversed(result))
