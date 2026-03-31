from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True
    
    def get_apartment_costs(self, apartment_key, year =None, month = None):
        if apartment_key not in self.apartments:
            return None
        total = 0
        for bill in self.bills:
            if apartment_key != bill.apartment:
                continue
            if month != bill.settlement_month and  month != None:
                continue
            if year != bill.settlement_year and year != None:
                continue
            total += bill.amount_pln

        return total
    
    def get_settlment_costs(self, apartment_key, year =None, month = None):
        settlment = ApartmentSettlement(
            apartment = apartment_key,
            year = year,
            month = month
            total_bills_pln = self.get_apartment_costs( apartment_key, year, month)
            total_rent_pln = 
            total_due_pln = 
        )
    



    
