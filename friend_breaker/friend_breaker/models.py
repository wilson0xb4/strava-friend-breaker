from django.db import models


class Athlete(models.Model):
    strava_id = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    # strava time strings
    newest_activity_date = models.CharField(max_length=20)
    oldest_activity_date = models.CharField(max_length=20)


# future ideas
#
# class Activity(models.Model):
#     strava_id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=200)
#     distance
#     start_latlng
#     end_latlng
#     average_speed
# class Segment(models.Model):
#     strava_id = models.IntegerField(primary_key=True)
#     name = models.CharField(max_length=50)
#     start_latlng
#     end_latlng
#     distance


class ChallenegedSegments(models.Model):
    my_id = models.IntegerField()
    their_id = models.IntegerField()
    their_name = models.CharField(max_length=50)

    my_pr = models.IntegerField()
    their_pr = models.IntegerField()

    my_time = models.CharField(max_length=8)
    their_time = models.CharField(max_length=8)
    difference = models.CharField(max_length=8)

    segment_id = models.IntegerField()
    segment_name = models.CharField(max_length=100)
    segment_distance = models.CharField(max_length=10)


