import random
from faker import Faker
from datetime import datetime, timedelta

from get_time import generate_time

fake = Faker()



def generate_fake_history(num_entries):
    history = []
    for _ in range(num_entries):
        title = fake.sentence(nb_words=8)  # Tạo tiêu đề ngẫu nhiên
        url = fake.url()  # Tạo URL ngẫu nhiên
        history.append([title, url, generate_time()])

    # print(history)
    return history