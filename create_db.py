import pandas as pd

file_1 = pd.read_csv('./data_file/제주특별자치도_제주시내버스노선현황_20221231.txt')
csv_file = file_1.to_csv('./data_file/제주특별자치도_제주시내버스노선현황_20221231.csv')
