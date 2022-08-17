from datetime import datetime
import json
from schema_validator.validator import validate


import pdb


with open('models/customer.json', 'r') as j:
    src_file_schema = json.loads(j.read())

schema = {
  "_id":          "ObjectId",
  "created":      "date",
  "is_active":    "bool",
  "fullname":     "string"
}

   
#pdb.set_trace()
isValid = validate(schema, src_file_schema)
for err in isValid:
    print(err['msg'])