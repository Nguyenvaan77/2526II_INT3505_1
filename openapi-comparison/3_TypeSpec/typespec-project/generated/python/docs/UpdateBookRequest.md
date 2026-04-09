# UpdateBookRequest

Request cập nhật sách

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** |  | [optional] 
**author_name** | **str** |  | [optional] 
**description** | **str** |  | [optional] 

## Example

```python
from openapi_client.models.update_book_request import UpdateBookRequest

# TODO update the JSON string below
json = "{}"
# create an instance of UpdateBookRequest from a JSON string
update_book_request_instance = UpdateBookRequest.from_json(json)
# print the JSON string representation of the object
print(UpdateBookRequest.to_json())

# convert the object into a dict
update_book_request_dict = update_book_request_instance.to_dict()
# create an instance of UpdateBookRequest from a dict
update_book_request_from_dict = UpdateBookRequest.from_dict(update_book_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


