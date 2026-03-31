from src.models import Apartment
from src.manager import Manager
from src.models import Parameters
from src.models import ApartmentSettlement

def test_load_data():
    parameters = Parameters()
    manager = Manager(parameters)
    assert isinstance(manager.apartments, dict)
    assert isinstance(manager.tenants, dict)
    assert isinstance(manager.transfers, list)
    assert isinstance(manager.bills, list)

    for apartment_key, apartment in manager.apartments.items():
        assert isinstance(apartment, Apartment)
        assert apartment.key == apartment_key

def test_tenants_in_manager():
    parameters = Parameters()
    manager = Manager(parameters)
    assert len(manager.tenants) > 0
    names = [tenant.name for tenant in manager.tenants.values()]
    for tenant in ['Jan Nowak', 'Adam Kowalski', 'Ewa Adamska']:
        assert tenant in names

def test_if_tenants_have_valid_apartment_keys():
    parameters = Parameters()
    manager = Manager(parameters)
    assert manager.check_tenants_apartment_keys() == True

    manager.tenants['tenant-1'].apartment = 'invalid-key'
    assert manager.check_tenants_apartment_keys() == False


def test_apartment_costs():
    parameters = Parameters()
    manager = Manager(parameters)
 
    assert manager.get_apartment_costs('apart-polanka', 2025, 1) == 910.0
    assert manager.get_apartment_costs('apart-polanka', 2025, 2) == 0.0
    assert manager.get_apartment_costs('polanka', 2025, 2) == None


def test_apartment_settlement_creation():
    parameters = Parameters()
    manager = Manager(parameters)

    settlement = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    assert isinstance(settlement, ApartmentSettlement) 
    assert settlement.apartment == 'apart-polanka'      
    assert settlement.year == 2025                      
    assert settlement.month == 1                       
    assert settlement.total_bills_pln == 910.0          
    assert settlement.total_due_pln == -910.0
    settlement_empty = manager.create_apartment_settlement('apart-polanka', 2025, 2)
    assert settlement_empty.total_bills_pln == 0.0      
    assert settlement_empty.total_due_pln == 0.0        
    assert settlement_empty.month == 2
    assert manager.create_apartment_settlement('nie-istnieje', 2025, 1) is None
