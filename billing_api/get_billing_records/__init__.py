# Import the get_record function from your DAL
from billing_data_access.data_access import get_record
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    record_id = req.route_params.get('id')
    partition_key = req.params.get('partitionKey')

    if not record_id or not partition_key:
        return func.HttpResponse("Missing record ID or partition key", status_code=400)

    record = get_record(record_id, partition_key)

    if record:
        return func.HttpResponse(json.dumps(record), mimetype="application/json", status_code=200)
    else:
        return func.HttpResponse("Record not found", status_code=404)

'''
fuction.json --- can modify route:

{
  "bindings": [
    {
      "authLevel": "function",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": ["get"],
      "route": "billing/{add id}"
    },
    {
      "type": "http",
      "direction": "out",
      "name": "$return"
    }
  ]
}

'''