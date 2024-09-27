from ebaysdk.finding import Connection as Finding

key = open("key.txt", "r").read()


# Returns eBay API results
def search(keyword):
    api = Finding(domain='svcs.sandbox.ebay.com', appid=key, config_file=None)
    out = api.execute('findItemsAdvanced', {'keywords': keyword})
    return out.dict()
