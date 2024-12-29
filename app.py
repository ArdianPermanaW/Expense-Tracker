import argparse
import csv
import calendar
from datetime import datetime

data = "data.csv"

parser = argparse.ArgumentParser()

parser.add_argument("command", type=str)
parser.add_argument("--description", type=str)
parser.add_argument("--amount", type=str)
parser.add_argument("--id", type=int)
parser.add_argument("--month", type=int)

args = parser.parse_args()

if args.command == "add":
    with open(data, mode="r", newline="") as file:
        reader = csv.reader(file)
        header = next(reader) # skip reading the header row
        rows = list(reader)
        if rows:
            addId = int(rows[-1][0]) + 1  
            
        else:
            addId = 1
    
    with open(data, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([addId,datetime.now().strftime('%Y-%m-%d'), args.description, args.amount])

    print(f"expense added succesfully (id:{addId})")

elif args.command == "list":
    with open (data, mode="r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        column_widths = [len(header) for header in headers]

        rows = list(reader)
        for row in rows:
            for i, cell in enumerate(row):
                column_widths[i] = max(column_widths[i], len(cell))
        
        print(" ".join(header.ljust(column_widths[i]) for i, header in enumerate(headers)))

        for row in rows:
            print(" ".join(cell.ljust(column_widths[i]) for i, cell in enumerate(row)))

elif args.command == "summary":
    summ = 0
    with open(data, mode="r", newline="") as file:
        reader = csv.DictReader(file)
        if args.month:
            for row in reader:
                if datetime.strptime(row['date'], '%Y-%m-%d').month == args.month:
                    summ += int(row['amount'])

            print(f"Total expenses for {calendar.month_name[args.month]}: {summ}")
        else:
            for row in reader:
                summ += int(row['amount'])
            print(f"Total expenses: {summ}")

elif args.command == "delete":
    with open(data, mode='r') as file:
        reader = csv.DictReader(file)
        rows = [row for row in reader if row['id'] != str(args.id)] 
    
    with open(data, mode='w', newline='') as file:
        fieldnames = ['id','date','description','amount'] 
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()  
        writer.writerows(rows) 
    
    print(f"Expense deleted successfully (id:{args.id})")
    
