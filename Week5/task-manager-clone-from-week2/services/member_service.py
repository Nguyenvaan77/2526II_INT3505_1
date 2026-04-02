from data import members


class MemberService:
    """Service xử lý logic liên quan đến Member"""
    
    @staticmethod
    def get_all_members():
        """Lấy tất cả thành viên"""
        return members
    
    @staticmethod
    def get_member_by_id(member_id):
        """Lấy thành viên theo ID"""
        member = next((m for m in members if m["id"] == member_id), None)
        return member
    
    @staticmethod
    def create_member(request):
        """Tạo thành viên mới"""
        new_id = max([m["id"] for m in members], default=0) + 1
        new_member = {
            "id": new_id,
            "name": request.name
        }
        members.append(new_member)
        return new_member
    
    @staticmethod
    def update_member(member_id, request):
        """Cập nhật thông tin thành viên"""
        member = MemberService.get_member_by_id(member_id)
        if not member:
            return None
        
        if request.name is not None:
            member["name"] = request.name
        
        return member
    
    @staticmethod
    def delete_member(member_id):
        """Xóa thành viên"""
        global members
        member = MemberService.get_member_by_id(member_id)
        if not member:
            return False
        
        members = [m for m in members if m["id"] != member_id]
        return True
