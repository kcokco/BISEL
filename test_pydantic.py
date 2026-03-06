import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from schemas import ReportCreate
from datetime import date

report = ReportCreate(
    watercourse_id="river",
    sampling_site_id="bridge",
    date=date.today(),
    quality_class="good",
    bisel_index=5,
    notes="none"
)
print("Before setting user_id:", report.model_dump())
report.user_id = 99
print("After setting user_id:", report.model_dump())
