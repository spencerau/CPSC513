import requests

urlAuction = "https://whiskyhunter.net/api/?format=openapi"

def list_all_auctions():
    print("Getting data...\n")
    response = requests.get("https://whiskyhunter.net/api/auctions_data/")
    
    if response.status_code == 200:
        data = response.json()
        unique_names = set()
        
        for record in data:
            name = record['auction_name']
            slug = record['auction_slug']
            
            if name not in unique_names:
                unique_names.add(name)
                url = f"https://whiskyhunter.net/auctions/{slug}"
                
                print(f"Name: {name}")
                print(f"Link: {url}")
                print(f"Slug: {slug}\n")
                
    else:
        print("Connection Failed, status code:", response.status_code)


def format(value):
    if not isinstance(value, (int, float)):
        raise ValueError("Input must be a numerical value")
    return f"£{value:,.2f}"


def get_details_auction_house():
    slug = input("Enter the slug of the auction house you wish to search for (use option 1 to find the slugs of each auction!)")
    print("Getting data...\n")
    url = "https://whiskyhunter.net/api/auction_data/"+slug+"/"
    print(url)
    print()
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for record in data:
            print(f"Date:     {record['dt']}")
            print(f"Max Bid:  {format(record['winning_bid_max'])}")
            print(f"Min Bid:  {format(record['winning_bid_min'])}")
            print(f"Mean Bid: {format(record['winning_bid_mean'])}\n")
    else:
        print("Connection Failed, staus code: ", response.status_code)


def get_fees_auction_house():
    slug = input("Enter the slug of the auction house you wish to search for (use option 1 to find the slugs of each auction!)")
    print("Getting data...")
    url = "https://whiskyhunter.net/api/auctions_info"
    print(url)
    print()
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for record in data:
            if slug == record['slug']:
                print(f"Buyers Fee:    {format(record['buyers_fee'])}")
                print(f"Sellers Fee:   {format(record['sellers_fee'])}")
                print(f"Reserve Fee:   {format(record['reserve_fee'])}")
                print(f"Listing Fee:   {format(record['listing_fee'])}")
                print(f"Base Currency: {record['base_currency']}")
    else:
        print("Connection Failed, staus code: ", response.status_code)


def list_all_distilleries():
    print("Getting data...\n")
    response = requests.get("https://whiskyhunter.net/api/distilleries_info/")

    if response.status_code == 200:
        data = response.json()
        unique = []
        for record in data:
            if record['name'] in unique:
                continue
            else:
                #print("Name: " + record['name'] + ", Slug: " + record['slug'])
                print(f"Name: {record['name']}")
                print(f"Slug: {record['slug']}\n")
                unique.append(record['name'])
    else:
        print("Connection Failed, staus code: ", response.status_code)


def get_details_distillery():
    slug = input("Enter the slug of the distillery you wish to search for (use option 4 to find the slugs of each distillery!)")
    print("Getting data...\n")
    url = "https://whiskyhunter.net/api/distillery_data/"+slug+"/"
    print(url)
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        for record in data:
            print(f"Date:     {record['dt']}")
            print(f"Max Bid:  {format(record['winning_bid_max'])}")
            print(f"Min Bid:  {format(record['winning_bid_min'])}")
            print(f"Mean Bid: {format(record['winning_bid_mean'])}\n")
    else:
        print("Connection Failed, staus code: ", response.status_code)


def run_app():
    while True:
        print("\n**Welcome to our alchol acution app! Powered by the WhiskeyHunter API.**\n")
        print("Would you like to:")
        print("1. List all stored auctions")
        print("2. List all bidding details of a specific auction house")
        print("3. List all fees and currency details of a specific auction house")
        print("4. List all stored distilleries")
        print("5. List all bidding details of a specific distillery")

        choice = input("\nEnter choice:")

        match choice:
            case "1": #auction_data/{slug}/
                list_all_auctions()

            case "2": #auctions_data/
                get_details_auction_house()

            case "3": #auctions_info
                get_fees_auction_house()

            case "4": #disterlleries_info
                list_all_distilleries()
                
            case "5": #disterllery data
                get_details_distillery()

            case _:
                print("Whoops! Thats not a proper option! " + choice)


if __name__ == "__main__":
    run_app()
