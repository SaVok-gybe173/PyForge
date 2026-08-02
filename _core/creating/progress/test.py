import os
print(os.__file__)
try:
    from PyForge._core.creating.progress.calculation_progress import ProgressBarCalc
except (ModuleNotFoundError, ImportError):
    from calculation_progress import ProgressBarCalc

data = ProgressBarCalc((100, 100), (422, 20))
data.set_percent(20)
print(data.get_percent(), data.get_pixel())
data.set_pixel(50)
print(data.get_percent(), data.get_pixel())
data.set_quantity_main(100),
data.set_quantity(50),
print(data.get_percent(), data.get_pixel())
data.del_quantity()
print(data.get_percent(), data.get_pixel())
data.set_percent(20)
print(data.get_percent(), data.get_pixel())

"""
20.0 84
20.0 50
50.0 211
50.0 211
20.0 84
"""
