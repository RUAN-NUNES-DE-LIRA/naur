from rest_framework import viewsets, decorators
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.request import Request

from courses.models import Course, Enrollment
from courses.serializers import CourseSerializer, ReviewSerializer
from courses.filters import CourseFilter

# Create your views here.

class CourseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    permission_classes = [AllowAny]
    filterset_class = CourseFilter
    ordering_fields = ['price', 'created_at']

    @decorators.action(detail=True, methods=['get'])
    def reviews(self, request: Request, pk=None):
        course = self.get_object
        reviews = course.reviews.all() 
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        enrolled_at = None

        if request.user.is_authenticated:
            enrolled = Enrollment.objects.filter(
                user=request.user,
                course=Course
            ).first()

            if enrolled:
                enrolled_at = enrolled.enrolled_at

        return Response({
            **serializer.data,
            "enrolled_at": enrolled_at
        })







































