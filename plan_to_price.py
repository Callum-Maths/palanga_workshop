import pandas as pd

class plan_to_price():
    def __init__(self, current_plan, current_vases, current_price, current_VOS, plan_offered, vases_offered, age_group, region, watching_hours):
        
        self.current_plan = current_plan
        self.current_vases = current_vases
        self.current_price = current_price
        self.current_VOS = current_VOS
        self.plan_offered = plan_offered
        self.vases_offered = vases_offered
        self.age_group = age_group
        self.region = region
        self.watching_hours = watching_hours

    def stage_one(self):
        plan_df = pd.read_csv('plans_offer_catalog.csv')
        vas_df = pd.read_csv('vas_offer_catalog.csv')

        possible_plans = plan_df[plan_df['rate_plan'] == self.plan_offered]
        if possible_plans.empty:
            print("Invalid plan offered.")
        else:
            plan_index = possible_plans.shape[0]
            if plan_index == 1:
                index = 0
                plan_standard_price = possible_plans.iloc[0]['price_norm']

            elif plan_index % 2 == 1:
                index = plan_index // 2
                plan_standard_price = possible_plans.iloc[plan_index // 2]['price_norm']
            else:
                index = plan_index // 2 - 1
                plan_standard_price = possible_plans.iloc[plan_index // 2 - 1]['price_norm']

            self.plan_index = plan_index
            self.index = index
            self.plan_standard_price = plan_standard_price
        
        def stage_two(self):
            "We will change this logic gates based on the statistics from previous sections"
            count = 0

            if self.watching_hours < 100:
                count -= 1
            if self.watching_hours > 500:
                count += 1

            if self.age_group == '40-49 y.o.' or self.age_group == '50-59 y.o.':
                count += 1
            
            if self.current_VOS < 0.1:
                count -= 1
            if self.current_VOS > 0.5:
                count += 1

            self.index += count
            if self.index < 0:
                self.index = 0
            elif self.index >= self.plan_index:
                self.index = self.plan_index - 1

            self.new_price = possible_plans.iloc[self.index]['price_norm']

            print(f"New price based on index {self.index}: {self.new_price}")
            


pricing_instance = plan_to_price(
    current_plan="plan_3",
    current_vases="",
    current_price=10.0,
    current_VOS=5,
    plan_offered="plan_3",
    vases_offered="Movies",
    age_group="Adult",
    muniplicity=1,
    watching_hours=2
)
pricing_instance.stage_one()

print('done')
