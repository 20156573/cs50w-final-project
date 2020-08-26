import re
from django.utils import timezone

def no_accent_vietnamese(s):
    s = s.encode().decode('utf-8')
    s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
    s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
    s = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', s)
    s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
    s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
    s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
    s = re.sub(u'[ìíịỉĩ]', 'i', s)
    s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
    s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
    s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
    s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
    s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
    s = re.sub(u'Đ', 'D', s)
    s = re.sub(u'đ', 'd', s)
    return s.encode('utf-8').decode("utf-8")

def get_how_long(s, x):
    now = timezone.now()
    before = x
    delta = now - before
    if delta.days == 0:
        if delta.seconds < 60:
            return f"{delta.seconds} giây trước"
        elif 60 <= delta.seconds < 3600:
            return f"{int(delta.seconds/60)} phút trước"
        return f"{int(delta.seconds/3600)} tiếng trước"
    return f"{delta.days} ngày trước"

def get_date(s, x):
    before = x
    return f"{before.day}-{before.month}-{before.year}"
