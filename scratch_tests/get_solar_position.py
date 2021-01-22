from pysolar.solar import *
import datetime


date = datetime.datetime(year=2021, month=1, day=22, hour=14, minute=34, second=1, tzinfo=datetime.timezone.utc)
print(get_altitude(42.206, -71.382, date))

