from ebaysdk.finding import Connection as Finding

key = open("key.txt", "r").readlines()

api = Finding(domain='svcs.sandbox.ebay.com', appid=key, config_file=None)

# Returns the total number of entries for a given query
# Uses 1 call
def total_entries(query: str):
    out = api.execute('findItemsAdvanced', {'keywords': query})
    return int(out.dict()['totalEntries'])

# Returns API results for all pages
# Uses n calls
def search(query: str, entries: int):
    result = []
    pages =

    # First page
    out = api.execute('findItemsAdvanced', {'keywords': query})
    d = out.dict()
    result.extend(d['searchResult'])

    if pages
        totalPages = d['paginationOutput']['totalPages']
        if pages > totalPages:
            pages = totalPages

        # Second to n-th page
        for p in range(2, page+1):
            out = api.execute('findItemsAdvanced', {'keywords': query, "paginationInput.pageNumber": p})
            d = out.dict()
            result.extend(d['searchResult'])

    return result
