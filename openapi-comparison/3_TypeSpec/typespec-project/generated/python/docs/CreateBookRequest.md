# CreateBookRequest

Request tạo sách

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | 
**author_name** | **str** |  | 
**description** | **str** |  | 

## Example

```python
from openapi_client.models.create_book_request import CreateBookRequest

# TODO update the JSON string below
json = "{}"
# create an instance of CreateBookRequest from a JSON string
create_book_request_instance = CreateBookRequest.from_json(json)
# print the JSON string representation of the object
print(CreateBookRequest.to_json())

# convert the object into a dict
create_book_request_dict = create_book_request_instance.to_dict()
# create an instance of CreateBookRequest from a dict
create_book_request_from_dict = CreateBookRequest.from_dict(create_book_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


