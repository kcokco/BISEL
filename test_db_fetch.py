import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from schemas import Report
from models import Report as DBReport
from database import SessionLocal

db = SessionLocal()
try:
    reports = db.query(DBReport).all()
    print("Found reports:", len(reports))
    for r in reports:
        # Simulate Pydantic validation
        validated = Report.model_validate(r)
        print("Validated:", validated.id)
except Exception as e:
    import traceback
    traceback.print_exc()
finally:
    db.close()
