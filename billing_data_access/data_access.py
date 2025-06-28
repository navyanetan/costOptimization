'''
Initialize Cosmos DB client using URI and KEY
Initialize reference

Initialize Blob Storage client using connection string
Initialize reference to billing-archive

Function get_record(record_id, partition_key):
    Fetch item from Cosmos DB using record_id and partition_key

    If item is found:
        Return item

    Else:
        Try to open blob from Blob Storage with name "<record_id>.json"
        Parse blob content as JSON
        Return parsed JSON

    If any error occurs:
        Return None

'''