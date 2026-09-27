import csv

def load_schedule_from_csv(file_path):
    """从CSV文件读取课表"""
    schedule_list = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            # 使用DictReader，这样可以通过列名访问数据
            reader = csv.DictReader(file)
            for row in reader:
                schedule_list.append({
                    'course': row['课程名'],
                    'day': row['星期几'],
                    'start': row['开始时间'],
                    'end': row['结束时间']
                })
        return schedule_list
    except FileNotFoundError:
        print(f"错误：找不到文件 {file_path}")
        return []

def print_schedule_view(schedule_list):
    """输出【本次课表】的文本视图"""
    print("\n===== 【本次课表】文本视图 =====")
    if not schedule_list:
        print("课表为空。")
        return
    
    # 按星期几和开始时间简单排个序
    schedule_list.sort(key=lambda x: (x['day'], x['start']))
    
    for item in schedule_list:
        print(f"[{item['day']}] {item['start']} - {item['end']} | {item['course']}")
    print("===============================\n")

def main():
    print("欢迎使用课表解析工具！")
    # 需求1：从CSV读入
    csv_file = "schedule.csv"
    schedule = load_schedule_from_csv(csv_file)
    
    # 需求1：引出文本视图
    print_schedule_view(schedule)

if __name__ == "__main__":
    main()