import csv, json

# goes through all the additions in our MSP board and produces two csv files going over the totals
#   and each individual additions profit, cost, amount paid, descriptions, productID, client, etc. 
#   go to the additions page in Connectwise and filter type by Managed Service, export the view and 
#   save as additionsearchscreen.csv in the Additions-Audit-Data folder. You will need to do the same
#   with the procurement-->product catalog, save this view as ProductSetupList.csv in the Additions-Audit-Data
#   You can then run this  program and produce the two reports discussed above. They will be named
#   clean_additions_individuals.csv and clean_additions_totals.csv within Auditions-Audit-Data

addition_file = open("Additions-Audit-Data/additionsearchscreen.csv", "r")
additions = csv.reader(addition_file)

addition_objs = []
for count, row in enumerate(additions):
    if count == 0:
        continue

    cycle = row[10]
    quantity = float(row[14])
    unit_price = float(row[17])
    cost = float(row[18]) * float(row[14])

    # ensuring the data is month by month
    if cycle == "Annual":
        unit_price = (unit_price / 12)
    elif cycle == "Quarterly":
        unit_price = (unit_price / 3)
        
    addition_objs.append({
        "product": row[2],
        "description": row[3],
        "company": row[6],
        "quantity": row[14],
        "unit_price": unit_price,
        "unit_cost": row[18]
    })

del addition_objs[0]

# For the costs of each individual additions
products_file = open("Additions-Audit-Data/ProductSetupList.csv", "r")
products = csv.reader(products_file)

product_costs = {x[1]:x[4] for x in products}
product_costs['="WFMSP RMM"'] = 3.00
product_costs['="WFMSP Offsite Backup"'] = 20

# Seperating it into a dictionary with the company name as the key
companies_additions = {}
for addition in addition_objs:
    if addition['company'] not in companies_additions:
        companies_additions[addition['company']] = [addition]
    else:
        companies_additions[addition['company']].append(addition)


total_write_file = open("Additions-Audit-Data/clean_additions_totals.csv", "w", newline="")
total_csvwriter = csv.writer(total_write_file)

individual_write_file = open("Additions-Audit-Data/clean_additions_individuals.csv", "w", newline="")
individual_csvwriter = csv.writer(individual_write_file)

fields = ["Product", "Description", "Quantity", "Cost per unit", "Our Cost", "Amount Paid", "Profit"]
ind_fields = ["Client", "Product", "Description", "Quantity", "Cost per unit", "Our Cost", "Amount Paid", "Profit"]

total_csvwriter.writerow(fields)
individual_csvwriter.writerow(ind_fields)
addition_totals = {}
for company in companies_additions:
    for addition in companies_additions[company]:
        try: 
            total_paid = float(addition['quantity']) * float(addition['unit_price'])
            our_cost = float(addition['quantity']) * float(product_costs[addition['product']])
            
            profit = float(total_paid) - float(our_cost)

            # csv file that holds all additions and their individual calculations
            individual_csvwriter.writerow([company, addition['product'], addition['description'], 
                                        float(addition['quantity']), round(float(product_costs[addition['product']]), 2),
                                        round(float(our_cost), 2), round(float(total_paid), 2), round(float(profit), 2)])
            
            if addition['product'] not in addition_totals:
                addition_totals[addition['product']] = {
                    "quantity": float(addition['quantity']),
                    "description": addition['description'],
                    "cost_per_unit": round(float(product_costs[addition['product']]), 2), 
                    "our_cost": round(float(our_cost), 2), 
                    "amount_paid": round(float(total_paid), 2), 
                    "profit": round(float(profit), 2)
                }
            else:
                addition_totals[addition['product']]['quantity'] += float(addition['quantity'])
                addition_totals[addition['product']]['our_cost'] += round(float(our_cost), 2)
                addition_totals[addition['product']]['amount_paid'] += round(float(total_paid), 2)
                addition_totals[addition['product']]['profit'] += round(float(profit), 2)

        except KeyError as err:
            print(err)
            pass

# Overall csv file of each product
for product in addition_totals:
    total_csvwriter.writerow([product, addition_totals[product]['description'], addition_totals[product]['quantity'],
                        round(addition_totals[product]['cost_per_unit'], 2), round(addition_totals[product]['our_cost'], 2), 
                        round(addition_totals[product]['amount_paid'], 2),  round(addition_totals[product]['profit'], 2)])


