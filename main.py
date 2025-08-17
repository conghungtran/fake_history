import sqlite3
import os
import shutil
import random

from dir import get_profile_directories
from fake import generate_fake_history



def get_chrome_history_path():
    """Tìm đường dẫn đến file History của Chrome tùy theo hệ điều hành."""
    if os.name == "nt":  # Windows
        path = os.path.join(
            os.environ["LOCALAPPDATA"],
            "Google",
            "Chrome",
            "User Data",
            # "Default",
            # "History",
        )
    elif os.name == "posix":
        # Kiểm tra cho macOS trước
        mac_path = os.path.join(
            os.path.expanduser("~"),
            "Library",
            "Application Support",
            "Google",
            "Chrome",
            # "Default",
            # "History",
        )
        if os.path.exists(mac_path):
            return mac_path
        # Mặc định cho Linux
        path = os.path.join(
            os.path.expanduser("~"), ".config", "google-chrome", 
            # "Profile 1", "History"
        )
    else:
        raise NotImplementedError(f"Hệ điều hành {os.name} không được hỗ trợ.")

    if os.path.exists(path):
        return path
    else:
        raise FileNotFoundError("Không tìm thấy file History của Chrome.")





def add_to_chrome_history(title, url, visit_time, history_path):
    """Thêm một URL và tiêu đề vào lịch sử Chrome."""

    try:
        # history_path = get_chrome_history_path()
        # print(f"Đã tìm thấy file History tại: {history_path}")

    
        # Kết nối đến database
        conn = sqlite3.connect(history_path)
        cursor = conn.cursor()

        # --- Bước 1: Thêm vào bảng `urls` ---

        # Kiểm tra xem URL đã tồn tại chưa
        cursor.execute("SELECT id FROM urls WHERE url=?", (url,))
        result = cursor.fetchone()

        if result:
            url_id = result[0]
            print(f"URL '{url}' đã tồn tại với id: {url_id}")
        else:
            # Nếu chưa tồn tại, thêm mới
            cursor.execute(
                "INSERT INTO urls (url, title, visit_count, typed_count, last_visit_time, hidden) VALUES (?, ?, 1, 1, 0, 0)",
                (url, title)
            )
            url_id = cursor.lastrowid  # Lấy id của hàng vừa thêm
            print(f"Đã thêm URL '{url}' vào bảng urls với id: {url_id}")

        # --- Bước 2: Thêm vào bảng `visits` ---

        # Lấy thời gian hiện tại và chuyển đổi

        print(visit_time)
        cursor.execute("INSERT INTO visits (url, visit_time, from_visit, transition, segment_id, visit_duration) VALUES (?, ?, 0, 838860805, 0, 2223)",
                       (url_id, visit_time))
        # Thêm một bản ghi visit mới
        # transition type 83886080 = TYPED (người dùng gõ trực tiếp)
        # cursor.execute("INSERT INTO visits (url, visit_time, from_visit, transition, segment_id, visit_duration, incremented_omnibox_typed_score, opener_visit, originator_cache_guid) VALUES (?, ?, 0, 838860805, NULL, 0, 0, 0, 0, 0, 0)",
        #     (url_id, visit_time))
       

        print(f"Đã thêm một bản ghi visit cho id {url_id} vào lúc {visit_time}")

        # Lưu thay đổi và đóng kết nối
        conn.commit()
        conn.close()

        print("\nThành công! Đã thêm dữ liệu vào lịch sử Chrome.")
        print("Bây giờ bạn có thể mở lại Chrome để kiểm tra.")

    except sqlite3.OperationalError as e:
        print(f"\nLỖI: {e}")
        print(
            "Vui lòng đảm bảo rằng bạn đã ĐÓNG HOÀN TOÀN Google Chrome trước khi chạy script này."
        )
    except Exception as e:
        print(f"Đã xảy ra lỗi không mong muốn: {e}")


# --- THỰC THI ---
if __name__ == "__main__":
    # Thay đổi URL và tiêu đề bạn muốn thêm ở đây
    target_dir = get_chrome_history_path()

    print(target_dir)

    found_dirs = get_profile_directories(target_dir)

    print(found_dirs)
    fake_history = generate_fake_history(15)

    # # print(fake_history)

    for dir in found_dirs:
        fake_history = generate_fake_history(15)
        for history in fake_history:
            add_to_chrome_history(history[0], history[1], history[2], dir)
