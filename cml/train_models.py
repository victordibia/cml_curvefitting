

from lib.processor import Processor

proc = Processor()
proc.load_data()
proc.preprocess()
proc.get_prophet_trends()
