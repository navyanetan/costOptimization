'''
Define function 'main' with input parameter 'name'

Get cutoff_date = current_utc_time - 90_days

Connect to Cosmos DB using URI and Key
Connect to Blob Storage using connection string

Query Cosmos DB for items where 'timestamp' < cutoff_date

For each item:
    Upload item as JSON to Blob Storage with name = item.id.json
    Delete item from Cosmos DB using its id and partition key
    log them
    (use try and catch to avoid runtime possible errors)

Return count of successfully archived records
'''