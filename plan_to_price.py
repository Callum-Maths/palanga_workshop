import pandas as pd

class plan_to_price:
    def __init__(self, current_plan, current_vases, current_price, current_VOS, plan_offered, vases_offered, age_group, muniplicity, watching_hours):
        
        self.current_plan = current_plan
        self.current_vases = current_vases
        self.current_price = current_price
        self.current_VOS = current_VOS
        self.plan_offered = plan_offered
        self.vases_offered = vases_offered
        self.age_group = age_group
        self.muniplicity = muniplicity
        self.watching_hours = watching_hours

    def stage_one(self):
       