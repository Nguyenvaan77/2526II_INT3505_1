from data import addresses, authors


class AddressService:
    """Service xử lý logic liên quan đến Address"""
    
    @staticmethod
    def get_all_addresses():
        """Lấy tất cả địa chỉ"""
        return addresses
    
    @staticmethod
    def get_address_by_id(address_id):
        """Lấy địa chỉ theo ID"""
        address = next((a for a in addresses if a["id"] == address_id), None)
        return address
    
    @staticmethod
    def get_address_with_author(address_id):
        """Lấy địa chỉ và thông tin tác giả"""
        address = AddressService.get_address_by_id(address_id)
        if not address:
            return None
        
        author = next((a for a in authors if a["id"] == address["author_id"]), None)
        return {
            "address": address,
            "author": author
        }
    
    @staticmethod
    def get_addresses_by_author(author_id):
        """Lấy tất cả địa chỉ của một tác giả"""
        return [a for a in addresses if a["author_id"] == author_id]
    
    @staticmethod
    def create_address(request):
        """Tạo địa chỉ mới"""
        # Kiểm tra xem tác giả có tồn tại không
        author = next((a for a in authors if a["id"] == request.author_id), None)
        if not author:
            return None
        
        new_id = max([a["id"] for a in addresses], default=0) + 1
        new_address = {
            "id": new_id,
            "author_id": request.author_id,
            "city": request.city,
            "country": request.country
        }
        addresses.append(new_address)
        return new_address
    
    @staticmethod
    def update_address(address_id, request):
        """Cập nhật thông tin địa chỉ"""
        address = AddressService.get_address_by_id(address_id)
        if not address:
            return None
        
        if request.city is not None:
            address["city"] = request.city
        if request.country is not None:
            address["country"] = request.country
        
        return address
    
    @staticmethod
    def delete_address(address_id):
        """Xóa địa chỉ"""
        global addresses
        address = AddressService.get_address_by_id(address_id)
        if not address:
            return False
        
        addresses = [a for a in addresses if a["id"] != address_id]
        return True
