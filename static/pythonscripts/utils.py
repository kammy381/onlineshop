from datetime import datetime as dt
from time import time

# def format_date(dt_, fmt="%H:%M:%S:%f"):
#     return f"{dt_:{fmt}}"

def now():
    a=time()
    return a


# def now():
#     return dt.now().strftime('%M:%S:%f"')[:-4]

#.strftime('%M:%S:%f"')[:-4]

# def remove_class(element, class_name):
#     element.element.classList.remove(class_name)
#
#
# def add_class(element, class_name):
#     element.element.classList.add(class_name)