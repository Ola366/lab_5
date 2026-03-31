from src.models import Apartment, Bill, Parameters, Tenant, Transfer, ApartmentSettlement, TenantSettlement


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
    
    def create_apartment_settlement(self, apartment_key, year =None, month = None):
            
            if apartment_key not in self.apartments:
                return None
            bills_sum = self.get_apartment_costs(apartment_key, year, month)    
            total_due = 0.0 - bills_sum
            return ApartmentSettlement(
            apartment=apartment_key,
            year=year,
            month=month,
            total_bills_pln=bills_sum,
            total_rent_pln=0.0,
            total_due_pln=total_due

        )
    

    def create_tenant_settlements(self, apartment_settlement: ApartmentSettlement):
        active_tenants = [
            t for t in self.tenants.values() 
            if t.apartment == apartment_settlement.apartment
        ]
        if not active_tenants:
            return []
        bills_per_tenant = apartment_settlement.total_bills_pln / len(active_tenants)
        results = []
        for tenant in active_tenants:
            total = tenant.rent_pln + bills_per_tenant
            settlement = TenantSettlement(
                tenant=tenant.name,
                apartment_settlement=apartment_settlement.apartment,
                month=apartment_settlement.month,
                year=apartment_settlement.year,
                rent_pln=tenant.rent_pln,
                bills_pln=bills_per_tenant,
                total_due_pln=total,
                balance_pln=-total  # Bilans na razie ujemny (do zapłaty)
            )
            results.append(settlement)
            
        return results

    
