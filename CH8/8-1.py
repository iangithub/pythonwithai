import datetime
import pytz

taipei_timezone = pytz.timezone('Asia/Taipei')
now_taipei = datetime.datetime.now(taipei_timezone)
print(now_taipei.strftime("%Y年%m月%d日 %H點%M分"))
