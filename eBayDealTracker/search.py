from ebaysdk.finding import Connection as Finding
import pymysql.cursors

search_query = input("Enter your search query: ")

key = open("key.txt", "r").read()

api = Finding(domain='svcs.sandbox.ebay.com', appid=key, config_file=None)
response = api.execute('findItemsAdvanced', {'keywords': search_query})

d = response.dict()

totalEntries = d['paginationOutput']['totalEntries']

if totalEntries == '0':
    print('No items were found')
    exit()

bound = int(input("How many entries should be shown? There are " + totalEntries + " entries in total: "))

print(d)  # print dictionary for debugging

for index in range(0, bound):
    title = (d['searchResult']['item'][index]['title'])  # item title
    itemId = (d['searchResult']['item'][index]['itemId'])  # item ID
    price = (d['searchResult']['item'][index]['sellingStatus']['currentPrice']['value'])  # item price
    viewItemURL = (d['searchResult']['item'][index]['viewItemURL'])  # URL to view item

    categoryId = int((d['searchResult']['item'][index]['primaryCategory']['categoryId']))  # return category Id

    if categoryId == 9355 and search_query == 'iphone':
        # Connect to the database
        connection = pymysql.connect(host='localhost',
                                     user="",
                                     password="",
                                     database='product_info',
                                     cursorclass=pymysql.cursors.DictCursor)

        with connection:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "INSERT INTO `filtered_product_info` (`title`, `itemId`, `price`, `viewItemURL`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (title, itemId, price, viewItemURL))

            # connection is not autocommit by default. So you must commit to save changes.
            connection.commit()
