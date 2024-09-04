from typing import Tuple,List,Union
from enum import Enum
import pytz
from datetime import datetime
from collections import OrderedDict
class COCOLabels(Enum):
    """
       Enumeration of label categories based on the COCO dataset.

       This enumeration represents common object categories.
       It's used for labeling and identifying objects in images.

       Attributes:
           PERSON (int): Represents the category for 'person'.
           CROWD (int): Represents the category for 'crowd'.
           MOPPING_BROWNING (int): Represents a custom or specific category,
                                   likely related to an activity or object.





    
    
    NUMPLATE = 0
    NUMPLATE_1 = 1
    PERSON = 2
    CAR = 3
    BIKE = 4
    TRUCK = 5
    AUTO = 6
    BUS = 7
    """
    HELMET = 0
    MASK = 1
    NO_HEALMET = 2
    NO_MASK = 3
    NO_VEST = 4
    PERSON = 5
    SAFETY_CONE = 6
    VEST = 7
    MACHINERY = 8
    VEHICLE = 9
class ColorLabels(Enum):
    """     Class vise color code  """
    """
    NUMPLATE: Tuple[int, int, int] = (0, 255, 0)
    NUMPLATE_1: Tuple[int, int, int] = (0, 255, 0)
    PERSON: Tuple[int, int, int] = (255, 0, 0)
    CAR: Tuple[int, int, int] = (0, 0, 255)
    BIKE: Tuple[int, int, int] = (0, 0, 255)
    TRUCK: Tuple[int, int, int] = (0, 0, 255)
    AUTO: Tuple[int, int, int] =  (0, 0, 255)
    BUS: Tuple[int, int, int] =  (0, 0, 255)

    """
    HELMET: Tuple[int, int, int] = (0, 255, 0)
    MASK: Tuple[int, int, int] = (0, 255, 0)
    NO_HEALMET: Tuple[int, int, int] = (0, 0, 255)
    NO_MASK: Tuple[int, int, int] = (0, 0, 255)
    NO_VEST: Tuple[int, int, int] = (0, 0, 255)
    PERSON: Tuple[int, int, int] = (0, 255, 0)
    SAFETY_CONE: Tuple[int, int, int] = (0, 255, 0)
    VEST: Tuple[int, int, int] = (0, 255, 0)
    MACHINERY: Tuple[int, int, int] = (0, 255, 0)
    VEHICLE: Tuple[int, int, int] = (0, 255, 0)
    
    
class Common:
    """Common Operation Class"""
    @staticmethod
    def center_of_bonding(box: List) -> Tuple[int,int]:
        """Find the absolute center of box"""
        x1, y1, x2, y2 = [int(i) for i in box]
        return (int(0.5 * (x1 + x2)), int(0.5 * (y1 + y2)))

    @staticmethod
    def bottom_center_of_bonding(box: List) -> Tuple[int,int]:
        """ Find the absolute bottom center of box """
        x1, y1, x2, y2 = [int(i) for i in box]
        return (int(0.5 * (x1 + x2)), y2)

    @staticmethod
    def is_point_inside_region(point: Tuple[int,int], region: List[int]) -> bool:
        """ Find the point inside the rectangle(region) """
        x_coord, y_coord = point
        xmin, ymin, xmax, ymax = region
        return xmin <= x_coord <= xmax and ymin <= y_coord <= ymax

class CUSTOM_DT:
    @staticmethod
    def g_c_ist_dt(Type :str="str",zone: str="IST" ) -> Union[str, datetime]:
        timezone_mapping = {
                            'UTC': 'UTC',
                            'IST': 'Asia/Kolkata',
                            }
        if zone not in timezone_mapping:
            raise ValueError("Invalid timezone. Use 'UTC' or 'IST'.")
        current_datetime = datetime.now(pytz.timezone(timezone_mapping[zone]))
        if Type=="str":
            return current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif Type == 'obj':
            return current_datetime
        else:
            raise ValueError("Invalid output_format. Use 'string' or 'datetime'.")

    @staticmethod
    def g_c_date(Type :str="str") -> Union[str, datetime.date]:
        current_date = datetime.now().date()
        if Type == "str":
            return current_date.strftime("%Y-%m-%d")
        elif Type == 'obj':
            return current_date

    @staticmethod
    def g_c_hour(Type :str="str",zone: str="IST" ) -> str:
        timezone_mapping = {
                            'UTC': 'UTC',
                            'IST': 'Asia/Kolkata',
                            }
        if zone not in timezone_mapping:
            raise ValueError("Invalid timezone. Use 'UTC' or 'IST'.")
        current_datetime = datetime.now(pytz.timezone(timezone_mapping[zone]))
        if Type=="str":
            return current_datetime.strftime("%H")
        else:
            raise ValueError("Invalid output_Type. Use 'str'")

    @staticmethod
    def g_custom_time(Type :str="str",zone: str="IST", hour: int=0,minute: int=0,second=0,microsecond: int=0):
        timezone_mapping = {
            'UTC': 'UTC',
            'IST': 'Asia/Kolkata',
        }
        if zone not in timezone_mapping:
            raise ValueError("Invalid timezone. Use 'UTC' or 'IST'.")
        current_datetime = datetime.now(pytz.timezone(timezone_mapping[zone]))
        current_datetime = current_datetime.replace(hour=hour,minute=minute,second=second,microsecond=
                                                    microsecond)
        if Type=="str":
            return current_datetime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        elif Type == 'obj':
            return current_datetime
        else:
            raise ValueError("Invalid output_format. Use 'string' or 'datetime'.")


    @staticmethod
    def calculate_duration_in_minutes(from_datetime_str: str, to_datetime_str: str) -> Union[int,float]:
        """
        Calculates the duration between two datetime strings and returns the duration in minutes.
        """
        # Define the datetime format
        datetime_format = "%Y-%m-%dT%H:%M:%S.%fZ"
        # Convert string to datetime objects
        from_datetime = datetime.strptime(from_datetime_str, datetime_format)
        to_datetime = datetime.strptime(to_datetime_str, datetime_format)
        # Convert datetimes to UTC
        utc_timezone = pytz.timezone('UTC')
        from_datetime_utc = from_datetime.replace(tzinfo=utc_timezone)
        to_datetime_utc = to_datetime.replace(tzinfo=utc_timezone)
        # Calculate duration
        duration = to_datetime_utc - from_datetime_utc
        # Convert duration to minutes and return
        return duration.total_seconds() / 60.0


class LimitedSizeDict(OrderedDict):
    """
        A dictionary with a limited size. When the size limit is reached,
        the oldest item is automatically removed when a new item is added.

        Attributes:
            size_limit (int): The maximum number of items this dictionary can hold.
    """
    def __init__(self, size_limit: int=30, *args, **kwargs):
        """
                Initializes the LimitedSizeDict with a specified size limit.

                Args:
                    size_limit (int): The maximum number of items the dictionary can hold.
                    *args: Variable length argument list.
                    **kwargs: Arbitrary keyword arguments.
        """
        self.size_limit:int = size_limit
        super().__init__(*args, **kwargs)

    def __setitem__(self, key, value):
        """
                Sets the item in the dictionary with the provided key and value.
                If adding the new item exceeds the size limit, the oldest item is removed.

                Args:
                    key: The key for the item to be set.
                    value: The value for the item to be set.
        """
        while len(self) >= self.size_limit:
            self.popitem(last=False)
        OrderedDict.__setitem__(self, key, value)


