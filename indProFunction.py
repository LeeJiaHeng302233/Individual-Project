import pandas as pd 
import os

def verify_user(ic, password):
    if len(ic) != 12 or not ic.isdigit() or password != ic[-4:]:    #make sure ic has 12 char / is number / ic = last 4 digit
        return False

    records = file_read_from_csv(filename = 'data/indpro_tax_records.csv')                          #get tax record from csv
    if not records:
        return False

    for record in records:
        record_ic = str(record.get('IC Number')).zfill(12).strip()  #compare ic input with IC Number in CSV
        if record_ic == ic:
            return True
        
def calculate_tax(income, relief):
    taxable = max(0.0, income - relief)                             #table of tax rate based on income
    taxrate = [
        (5000, 0.0),
        (20000, 0.01),
        (35000, 0.03),
        (50000, 0.06),
        (70000, 0.11),
        (100000, 0.19),
        (400000, 0.25),
        (600000, 0.26),
        (2000000, 0.28),
        (float('inf'), 0.30)
    ]
    tax = 0.0
    prev_limit = 0.0
    for limit, rate in taxrate:
        if taxable <= prev_limit:
            break
        taxable_amount = min(taxable, limit) - prev_limit
        tax += taxable_amount * rate
        prev_limit = limit                                          # Calculate taxable income
    return tax

def save_to_csv(data, filename):
    try:
        ip = pd.DataFrame(data)
        if 'IC Number' in ip.columns:
            ip['IC Number'] = ip['IC Number'].apply(lambda x: str(x).zfill(12))
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        ip.to_csv(filename, index=False)                            #saves everything in ip to CSV, data automatically become columns in the DataFrame 
    except Exception as e:
        print(f"Error saving data: {e}")                            # save IC into CSV as string, keep 0 on the left of IC numbers, CSV always remove leading zeros...

def file_read_from_csv(filename):
    if not os.path.exists(filename):
        return None
    try:
        ip = pd.read_csv(filename, dtype={'IC Number': str})
        ip['IC Number'] = ip['IC Number'].apply(lambda x: str(x).zfill(12))
        num_cols = ["Income", "Tax Relief", "Tax Payable"]
        for col in num_cols:
            if col in ip.columns:
                ip[col] = pd.to_numeric(ip[col], errors='coerce').fillna(0.0)
        return ip.to_dict('records')
    except Exception as e:
        print(f"Error reading file: {e}")
        return None                                                 # match IC number to each record, if the value is not numbers or blank, replace with Not a Number (NaN)
