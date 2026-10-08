import json, os

resources = {
    "R001": {"id": "R001", "name": "Laptop", "category": "Electronics", "total": 10, "available": 10},
    "R002": {"id": "R002", "name": "Keyboard", "category": "Accessories", "total": 5, "available": 5},
    "R003": {"id": "R003", "name": "Headset", "category": "Accessories", "total": 3, "available": 3}
}
fellows = {"F001": "Ada", "F002": "John", "F003": "Grace"}
borrow_records = []
DATA_FILE = "campus_data.json"

def get_borrowed_qty(fellow_id, resource_id):
    return sum(r["quantity"] for r in borrow_records if r["fellow_id"]==fellow_id and r["resource_id"]==resource_id)

def list_resources():
    print("\n--- INVENTORY ---")
    for r in resources.values():
        print(f'{r["id"]} | {r["name"]} ({r["category"]}) | Total: {r["total"]} | Available: {r["available"]}')

def add_resource():
    rid = input("Enter ID: ").strip().upper()
    if rid in resources:
        print(f"Error: Duplicate ID {rid} rejected.")
        return
    name = input("Enter name: ").strip()
    category = input("Enter category: ").strip()
    try:
        total = int(input("Enter total: ").strip())
        if total <= 0: raise ValueError
    except:
        print("Error: Total must be positive integer"); return
    resources[rid] = {"id": rid, "name": name, "category": category, "total": total, "available": total}
    print(f"Added {name}")

def borrow_resource(f_id=None, r_id=None, qty=None):
    if f_id is None: f_id = input("Fellow ID: ").strip().upper()
    if r_id is None: r_id = input("Resource ID: ").strip().upper()
    if qty is None:
        try: qty = int(input("Quantity: ").strip())
        except: print("Error: Quantity must be number"); return False
    if f_id not in fellows: print(f"Error: Fellow {f_id} not found"); return False
    if r_id not in resources: print(f"Error: Resource {r_id} not found"); return False
    if not isinstance(qty,int) or qty<=0: print("Error: Quantity must be positive integer"); return False
    if qty > resources[r_id]["available"]:
        print(f"Rejected: Only {resources[r_id]['available']} available, requested {qty}. Stock unchanged."); return False
    resources[r_id]["available"] -= qty
    borrow_records.append({"fellow_id": f_id, "resource_id": r_id, "quantity": qty})
    print(f"SUCCESS: {fellows[f_id]} borrowed {qty} x {resources[r_id]['name']}. Available now: {resources[r_id]['available']}")
    return True

def return_resource(f_id=None, r_id=None, qty=None):
    if f_id is None: f_id = input("Fellow ID: ").strip().upper()
    if r_id is None: r_id = input("Resource ID: ").strip().upper()
    if qty is None:
        try: qty = int(input("Quantity to return: ").strip())
        except: print("Error: Quantity must be number"); return False
    if f_id not in fellows: print(f"Error: Fellow {f_id} not found"); return False
    if r_id not in resources: print(f"Error: Resource {r_id} not found"); return False
    if not isinstance(qty,int) or qty<=0: print("Error: Quantity must be positive"); return False
    has = get_borrowed_qty(f_id, r_id)
    if qty > has:
        print(f"Rejected: {f_id} only has {has} on loan, tried to return {qty}. Stock unchanged."); return False
    resources[r_id]["available"] += qty
    rem = qty
    for rec in reversed(borrow_records):
        if rec["fellow_id"]==f_id and rec["resource_id"]==r_id and rem>0:
            d = min(rec["quantity"], rem)
            rec["quantity"] -= d
            rem -= d
    borrow_records[:] = [r for r in borrow_records if r["quantity"]>0]
    print(f"SUCCESS: Returned {qty} x {resources[r_id]['name']}. Available now: {resources[r_id]['available']}")
    return True

def search_resources(term=None):
    if term is None: term = input("Search name: ").strip()
    found = [r for r in resources.values() if term.lower() in r["name"].lower()]
    for r in found: print(f'Found: {r["id"]} - {r["name"]}')
    if not found: print("No match")
    return found

def filter_by_category(cat=None):
    if cat is None: cat = input("Filter category: ").strip()
    found = [r for r in resources.values() if cat.lower() == r["category"].lower()]
    for r in found: print(f'{r["id"]} - {r["name"]} ({r["category"]})')
    if not found: print("No resources in that category")
    return found

def generate_report():
    total = sum(r["total"] for r in resources.values())
    avail = sum(r["available"] for r in resources.values())
    borrowed = total - avail
    low = [r for r in resources.values() if r["available"] < 3]
    b_map = {r["id"]: r["total"]-r["available"] for r in resources.values()}
    max_b = max(b_map.values()) if b_map else 0
    leaders = [resources[rid] for rid,q in b_map.items() if q==max_b and q>0]
    print("\n--- REPORT ---")
    print(f"Overall units {total}, Available {avail}, Borrowed {borrowed}")
    print(f"Low stock (<3): {', '.join([f'{r['name']} ({r['available']})' for r in low]) or 'None'}")
    print(f"Most borrowed ({max_b}): {', '.join([r['name'] for r in leaders]) or 'None'}")

def demo_sequence():
    print("\n=== DEMO STEPS 1-7 ===")
    print("1. F001 borrows 2 laptops — available laptop units = 8"); borrow_resource("F001","R001",2)
    print("2. F002 borrows 3 keyboards — available keyboard units = 2"); borrow_resource("F002","R002",3)
    print("3. F001 returns 1 laptop — available laptop units = 9"); return_resource("F001","R001",1)
    print("4. F003 requests 4 headsets — rejected without changing stock"); borrow_resource("F003","R003",4)
    print("5. F002 tries to return 4 keyboards — rejected without changing stock"); return_resource("F002","R002",4)
    print("6. Search for LAPtop — find Laptop, ignoring case"); search_resources("LAPtop")
    print("7. Generate the report — overall units 18, available 14, borrowed 4, Keyboard low stock (2); Keyboard is most borrowed (3)"); generate_report()

def main():
    while True:
        print("\n[1] List [2] Add [3] Borrow [4] Return [5] Search [6] Filter [7] Report [8] DEMO 1-7 [9] Save [10] Load [0] Exit")
        ch = input("Choice: ").strip()
        if ch=="1": list_resources()
        elif ch=="2": add_resource()
        elif ch=="3": borrow_resource()
        elif ch=="4": return_resource()
        elif ch=="5": search_resources()
        elif ch=="6": filter_by_category()
        elif ch=="7": generate_report()
        elif ch=="8": demo_sequence()
        elif ch=="9":
            with open(DATA_FILE,"w") as f: json.dump({"resources":resources,"borrow_records":borrow_records},f,indent=2)
            print("Saved")
        elif ch=="10":
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE) as f:
                    d=json.load(f); resources.update(d["resources"]); borrow_records[:]=d["borrow_records"]
                print("Loaded")
            else: print("No file")
        elif ch=="0": break
        else: print("Invalid choice")

if __name__ == "__main__":
    main()