'''Define bucket schema used in parse_calendar.'''

from .bucket_schema import BucketSchema
from dateutil.parser import parse as parse_date

boston_calendar_schema = BucketSchema()
def schema_unknown(entry):
  try:
    parse_date(entry['time'])
  except:
    return True
  return False
boston_calendar_schema.add('Multi-Day', 8, lambda x: 'until' in x['time'])
boston_calendar_schema.add('Unknown',   9, schema_unknown)
boston_calendar_schema.add('Morning',   1, lambda x: parse_date(x['time']).hour < 12)
boston_calendar_schema.add('Afternoon', 2, lambda x: parse_date(x['time']).hour < 17)
boston_calendar_schema.add('Evening',   3, lambda x: parse_date(x['time']).hour < 19)
boston_calendar_schema.add('Night',     4, lambda x: True)