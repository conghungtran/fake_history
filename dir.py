import os
import re


def get_profile_directories(parent_directory):
    """
    Tìm tên của các thư mục con trong một thư mục cha theo định dạng "Profile N", 
    trong đó N là một số tự nhiên.
    Hàm sẽ loại trừ các file hoặc thư mục không khớp định dạng này (ví dụ: "Profile System").
    """
    
    # Biểu thức chính quy (Regular Expression) để khớp với "Profile N"
    # ^ : Bắt đầu chuỗi
    # Profile\s : Chuỗi "Profile " (có khoảng trắng)
    # \d+ : Một hoặc nhiều chữ số
    # $ : Kết thúc chuỗi
    pattern = r"^Profile\s\d+$"
    
    # Danh sách để lưu tên các thư mục phù hợp
    matching_directories = []

    # Kiểm tra xem thư mục cha có tồn tại không
    if not os.path.isdir(parent_directory):
        print(f"Lỗi: Thư mục '{parent_directory}' không tồn tại.")
        return matching_directories

    for item_name in os.listdir(parent_directory):
        # Tạo đường dẫn đầy đủ tới mục đó
        item_path = os.path.join(parent_directory, item_name)
        
        if os.path.isdir(item_path):
            # Nếu là thư mục, kiểm tra xem tên có khớp với mẫu "Profile N" không
            if re.fullmatch(pattern, item_name):
                matching_directories.append(f"{parent_directory}/{item_name}/History")
            
    return matching_directories

# target_dir = get_chrome_history_path()

# print(target_dir)

# found_dirs = get_profile_directories(target_dir)

# for dir in found_dirs:
#     print(dir)
