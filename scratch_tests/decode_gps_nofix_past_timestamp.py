from datetime import datetime

OUR_SPECIAL_EPOCH = 1577840461
CONSTANT_MINUTES_SINCE_EPOCH_NOFIX = 45285447
k = -680
DUMMY_VALUE_SENT_DOWN = 25534

PAST_TIMESTAMP_UNIX = (CONSTANT_MINUTES_SINCE_EPOCH_NOFIX + OUR_SPECIAL_EPOCH / 60 - DUMMY_VALUE_SENT_DOWN + k * 2 ** 16) * 60

print(PAST_TIMESTAMP_UNIX)


# if you encounter a "year is out of range" error the timestamp
# may be in milliseconds, try `ts /= 1000` in that case
print(datetime.utcfromtimestamp(PAST_TIMESTAMP_UNIX).strftime('%Y-%m-%d %H:%M:%S'))