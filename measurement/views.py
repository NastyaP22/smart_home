from django.forms import model_to_dict
from rest_framework.generics import ListAPIView
from rest_framework.response import Response

from measurement.models import Sensor, Measurement
from measurement.serializers import SensorDetailSerializer, MeasurementSerializer


class SensorView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

    def get(self, request):
        return Response({'Sensors': list(self.queryset.values())})

    def post(self, request):
        new_sensor = Sensor.objects.create(
            name = request.data['name'],
            description = request.data['description']
        )
        return Response({'new_sensor': model_to_dict(new_sensor)})

    def patch(self, request, pk):
        new_patch = Sensor.objects.get(id_exact=pk)
        if 'name' in request.data:
            new_patch.name = request.data['name']
        if 'description' in request.data:
            new_patch.description = request.data['description']
        new_patch.save()
        return Response({'new_patch': model_to_dict(new_patch)})


class MeasurementView(ListAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def get(self, request, pk):
        exact_sensor = Sensor.objects.get(id_exact = pk)
        measurements = Measurement.objects.filter(sensor_id = exact_sensor)
        response = model_to_dict(exact_sensor)
        response['measurements'] = [model_to_dict(measurement) for measurement in measurements]
        return Response(response)

    def post(self, request):
        new_post = Measurement.objects.create(
            sensor_id = Sensor.objects.get(id_exact = request.data['sensor_id']),
            temperature = request.data['temperature']
        )
        return Response({'new_post': model_to_dict(new_post)})