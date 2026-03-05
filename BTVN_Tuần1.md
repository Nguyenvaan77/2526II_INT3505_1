# 1. Google Maps Platform & Cloud Translation API
 - Dữ liệu: Dùng để lấy thông tin, dữ liệu, hình ảnh và ngôn ngữ thực tế
 - Đặc điểm dữ liệu: Dữ liệu dựa trên thế giới thực
 - Xác thực: Xác thực qua OAuth2.0 hoặc API Key (Với các dịch vụ đơn giản)
 - Định dạng: JSON
 - Chi phí: Miễn phí 200$ mỗi tháng, quá thì người dùng nạp để dùng tiếp
 - Các nhóm API: Maps (Dữ liệu địa lí), Routes (Dữ liệu điều hướng), Places (Dữ liệu)
 - Một vài API quan trọng: 
    + Place Autocomplete (Gợi ý địa chỉ khi gõ):
    https://maps.googleapis.com/maps/api/place/autocomplete/json?input=[Từ-khóa]&types=geocode&language=vi&key=YOUR_API_KEY

    + Nearby Search (Tìm địa điểm xung quanh tọa độ):
    https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=[Vĩ-độ],[Kinh-độ]&radius=1500&type=restaurant&key=YOUR_API_KEY

    + Place Details (Lấy thông tin chi tiết một địa điểm):
    https://maps.googleapis.com/maps/api/place/details/json?place_id=[Mã-địa-điểm]&fields=name,rating,formatted_phone_number&key=YOUR_API_KEY

# 2. Spotify Web API
- Dữ liệu: Dữ liệu âm nhạc, podcast và hành vi người dùng
- Đặc điểm dữ liệu: Có thuật toán gợi ý và thời gian thực 
- Xác thực: OAuth 2.0 bắt buộc để truy cập dữ liệu người dùng
- Định dạng: JSON chuẩn hóa RESTful
- Chi phí: Miễn phí
- Một vài API quan trọng: 
    + Search API (Tìm kiếm bài hát, nghệ sĩ, album):
    https://api.spotify.com/v1/search?q=[Từ-khóa]&type=[track,artist]&limit={limit}

    + Get Artist's Top Tracks (Lấy các bài hát "đỉnh" nhất của nghệ sĩ):
    https://api.spotify.com/v1/artists/{id}/top-tracks?market=VN

    + Get Recommendations (Gợi ý nhạc dựa trên sở thích):
    https://api.spotify.com/v1/recommendations?seed_artists=[ID]&seed_genres=pop&target_energy=0.8

# 3. Youtube Data API
- Dữ liệu: Dữ liệu video, kênh nội dung và tương tác cộng đồng
- Đặc điểm dữ liệu: Quản lí tài nguyên phân cấp 
- Xác thực: API Key với dữ liệu công khai và OAuth 2.0 với tác vụ Quản lí kênh
- Định dạng: JSON
- Chi phí: Miễn phí 10000 token / ngày
- Một vài API quan trọng: 
    + Search: list (Tìm kiếm video/kênh/playlist theo từ khóa):
    https://www.googleapis.com/youtube/v3/search?part=snippet&q=[Từ-khóa]&type=video&maxResults=10&key=YOUR_API_KEY

    + Videos: list (Lấy số lượt view, like, comment và tag):
    https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics,contentDetails&id=[VIDEO_ID]&key=YOUR_API_KEY

    + Channels: list (Lấy thông tin kênh):
    https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics,contentDetails&id=[CHANNEL_ID]&key=YOUR_API_KEY