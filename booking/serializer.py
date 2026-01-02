from rest_framework import serializers


class TrainSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50)
    number = serializers.IntegerField()


class SearchTrainSerializer(serializers.Serializer):
    source = serializers.CharField(max_length=50, required=True)
    destination = serializers.CharField(max_length=50, required=True)
    journey_date = serializers.DateField(required=True)


class PassengerSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=50, required=True)
    age = serializers.IntegerField(required=True)
    gender = serializers.CharField(max_length=10, required=True)
    status = serializers.CharField(default="Unassigned")


class BookSeatSerializer(serializers.Serializer):
    train_number = serializers.IntegerField(required=True)
    journey_date = serializers.DateField(required=True)
    source = serializers.CharField(max_length=50, required=True)
    destination = serializers.CharField(max_length=50, required=True)
    coach_type = serializers.CharField(max_length=20, required=True)
    passengers = PassengerSerializer(many=True, required=True)