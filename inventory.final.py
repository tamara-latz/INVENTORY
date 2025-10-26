store = input("What store are you: ")
print("Hello ", store, "!", sep='')
todays_date = input("Enters today's date with the format MMDDYYYY, (ex. December 5, 2005 >> 12052005): ")

number_aisles = int(input("Enter the number of aisles of the grocery store: "))
aisles = number_aisles * [0]


def display_menu():
    #prints a menu of options
    print()
    print('(0) Enter a new item')
    print('(1) Enter a sold, stolen, or disgarded item')
    print('(2) Change price')
    print('(3) Run inventory analysis')
    print('(4) Quit')
    

inventory = {}



""" Add item type to inventory, ex. granny smith apple """
def add_product_type(name, price, quantity, aisle, batch_ID, expiration):
    if name in inventory: #if product already exists in dictionary
        add_item(name, batch_ID, expiration, quantity)
    else:
        inventory[name] = { 
        "price": price,
        "quantity": quantity,
        "location": aisle,
        "items": {}}
        add_item(name, batch_ID, expiration, quantity)

""" Add individual item to inventory, ex. granny smith apple #5 """
def add_item(name, batch_ID, expiration, quantity):
     
    if "items" not in inventory[name]: #have to make sure its in it
        inventory[name]["items"] = {}
    
    inventory[name]["items"][batch_ID]= {"expiration": expiration, "amount": quantity } 

    inventory[name]["quantity"] += quantity #increment quantity
    return

""" Remove item from inventory when sold, stolen, or thrown away """
def remove_item(name, quantity, batch_ID):
    if (quantity > inventory[name]["quantity"] or quantity > inventory[name]["items"][batch_ID]["amount"]):
        raise Exception("Amount removed greater than total amount")
    else:
        inventory[name]["items"][batch_ID]["amount"] = inventory[name]["items"][batch_ID]["amount"] - quantity #item quantity

        inventory[name]["quantity"] = inventory[name]["quantity"] - quantity #total quantity

        return

def change_price(name, new_price):
    inventory[name]["price"] = new_price
    return

def change_quantity(name, new_quantity):
    inventory[name]["quantity"] = new_quantity
    return

def change_location(name, new_aisle):
    inventory[name]["location"] = new_aisle
    return

def change_expiration(name, batch_ID, new_expiration):
    inventory[name]["items"][batch_ID]["expiration"] = new_expiration
    return

""" BIG MAMA FUNCTION """
def inventory_analysis():
    products_expiring_soon = expire_soon()
    expired_products = expired()
    out_of_products = out_of()

    print("The following products expire soon: ", products_expiring_soon)
    answer = input ("Would you consider putting these products on sale? (answer yes or no): ")
    if answer == "no":
        print("I recommend donating these items to charity")
    if answer == "yes":
        sale_percent = float(input("Enter the percent you would like to discount the item (enter as a decimal: 50% = .50): "))
        print ("We put the products on sale")
        sale(products_expiring_soon, sale_percent)
        
    
    print("The following products are expired: ", expired_products)
    print("The following products should be reordered: ", out_of_products)

""" Calculates tomorrow's date """
def tomorrows_date():
    day = todays_date[2:4]
    month = todays_date[0:2]

    tomorrows_date = ""
    if ((month == 12) and day == 31):
        tomorrows_date = str(int(todays_date) + 1) #happy new year!

    elif ((month == "01" or month == "03" or month == "05" or month == "07" or month == "08" or month == "10") and day == "31"):
        tomorrows_date = str(int(todays_date) + 1000000) # increment month
        tomorrows_date = todays_date[0:2] + "01" + todays_date[4:] # increment day

    elif ((month == "04" or month == "06" or month == "09" or month == "11") and day == "30"):
        tomorrows_date = str(int(todays_date) + 1000000) # increment month
        tomorrows_date = tomorrows_date[0:2] + "01" + tomorrows_date[4:] # increment day

    elif ((month == "02" and day == "28") or (month == "02" and day == "29")):
        tomorrows_date = str(int(todays_date) + 1000000) # increment month
        tomorrows_date = tomorrows_date[0:2] + "01" + tomorrows_date[4:] # increment day

    else:
        tomorrows_date = str(int(todays_date) + 10000)
        
    return tomorrows_date

""" Returns dictionary of products expiring soon """
def expired():
    products_expired = {} #dictionary of products expiring soon
    # {name: ID, ID, ID, name: ID, ID, ID, etc}
    for name in inventory: # for loop iterating through each product's batches
        for batch_ID in inventory[name]["items"]:
            expiration = inventory[name]["items"][batch_ID]["expiration"]

            if(int(todays_date[4:]) > int(expiration[4:])): # if today's year after expiration year
                products_expired[name] = inventory[name]["items"][batch_ID]

            elif(int(todays_date[2:4]) > int(expiration[2:4])): # if today's month after expiration year
                products_expired[name] = inventory[name]["items"][batch_ID]

            elif(int(todays_date[0:2]) > int(expiration[0:2])): # if today's day after expiration
                products_expired[name] = inventory[name]["items"][batch_ID]
                
    return products_expired

def expire_soon():
    products_expiring_soon = {}
    next_day = tomorrows_date()

    for name in inventory: # for loop iterating through each product's batches
        for batch_ID in inventory[name]["items"]:
            expiration = str(inventory[name]["items"][batch_ID]["expiration"])
            if next_day == expiration:
                print ("Your product is expiring soon")
                products_expiring_soon[name] = inventory[name]["items"][batch_ID]
    return products_expiring_soon







#this function will increase the number at the index of the aisle if there is
#expired food in the aisle 
def increment_expired_aisle():
    #calling the function expired. This will give a dictionary. 
    #We will then go through the dictionary and increment the aisle that has the expired food

    for i in expired():
        aisle = inventory[i]["location"]
        aisles[aisle-1]+=1
        print ("you have an expired item in aisle ", aisle)
    return

def out_of():

    out_of = []
    for name in inventory:
        if (inventory[name]["quantity"] == 0):
            out_of.append(name)
    return out_of

def sale(products_expiring_soon, sale_percent):

    for name in inventory:
        for product in products_expiring_soon:
            if name == product:
                inventory[name]["price"] = inventory[name]["price"] * (1-sale_percent)


def main():
    "main user interaction loop"
    while True:
        display_menu()
        choice = int(input('Enter your choice: '))
        print()
            
        if choice == 0:
            name = input("Product name?: ")
            price = int(input("Product price?: "))
            quantity =int(input("Product quantity?: "))
            aisle = int(input("Product's aisle number?: "))
            batch_ID = int(input("Enter the products ID number: ")) 
            expiration = input("Product's expiration date? Format MMDDYYYY, ex. December 5, 2005 >> 12052005: ")
                
            add_product_type(name, price, quantity, aisle, batch_ID, expiration)
                
            print("New products added! Would you like to do anything else?: ")
        
            
        elif choice == 4:
            break
            
        elif choice == 1:
            name = input("Product name?: ")
            quantity = int(input("Product quantity?: "))
            batch_ID = int(input("Enter the batch ID of the product to remove: "))              
            remove_item(name, quantity, batch_ID)
                
            print("Sold, stolen, or disregarded products removed! Would you like to do anything else?: ")
                
        elif choice == 2:
            name = input("Enter the name of the item: ")
            new_price = int(input("Enter the new product price: "))
            change_price(name, new_price)
                
            print("Price updated! Would you like to do anything else?: ")
                
        elif choice == 3:
            inventory_analysis()
            print("Here is your inventory analysis! Would you like to do anything else?: ")


if __name__ == "__main__":
    main()
