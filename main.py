# 需求1：课表读取与文本视图
# 需求2：计算个人空闲时间段

import csv

# ================= 工具函数 =================
def time_to_minutes(time_str):
    """将 08:00 转换为分钟数 480"""
    h, m = map(int, time_str.split(':'))
    return h * 60 + m

def minutes_to_time(minutes):
    """将 480 转换为 08:00"""
    h = minutes // 60
    m = minutes % 60
    return f"{h:02d}:{m:02d}"

# ================= 需求1：读取课表 =================
def load_schedule_from_csv(file_path, person_name):
    """从CSV文件读取课表"""
    schedule_list = []
    try:
        with open(file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                schedule_list.append({
                    'person': person_name,
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
    schedule_list.sort(key=lambda x: (x['day'], x['start']))
    for item in schedule_list:
        print(f"[{item['day']}] {item['start']} - {item['end']} | {item['course']} (来自: {item['person']})")
    print("===============================\n")

# ================= 需求2：计算个人空闲时间 =================
def get_person_free_slots(person_schedule, day, day_start_min, day_end_min):
    """获取某个人在某天的空闲时间段（分钟数元组）"""
    day_courses = [c for c in person_schedule if c['day'] == day]
    day_courses.sort(key=lambda x: time_to_minutes(x['start']))
    
    free_slots = []
    current_time = day_start_min
    
    for course in day_courses:
        course_start = time_to_minutes(course['start'])
        course_end = time_to_minutes(course['end'])
        
        # 如果课程开始前有空闲时间（且 >= 30分钟）
        if course_start - current_time >= 30:
            free_slots.append((current_time, course_start))
        # 更新当前时间（取较晚的结束时间，防止课程重叠）
        current_time = max(current_time, course_end)
    
    # 最后一节课结束到晚上的空闲
    if day_end_min - current_time >= 30:
        free_slots.append((current_time, day_end_min))
    
    return free_slots

def print_all_free_times(schedule_list, day_start="08:00", day_end="22:00"):
    """打印每个人的空闲时间段"""
    print("===== 【所有人的空闲时间段】 =====")
    day_start_min = time_to_minutes(day_start)
    day_end_min = time_to_minutes(day_end)
    days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    # 按人分组
    people = list(set([c['person'] for c in schedule_list]))
    
    for person in people:
        print(f"--- {person} 的空闲时间 ---")
        person_schedule = [c for c in schedule_list if c['person'] == person]
        for day in days:
            slots = get_person_free_slots(person_schedule, day, day_start_min, day_end_min)
            if slots:
                slot_strs = [f"{minutes_to_time(s)} - {minutes_to_time(e)}" for s, e in slots]
                print(f"[{day}] 空闲: {', '.join(slot_strs)}")
    print("===============================\n")

# ================= 主程序 =================
def main():
    print("欢迎使用课表解析工具！")
    
    # 读取多个人的课表
    schedule_A = load_schedule_from_csv("schedule.csv", "同学A")
    schedule_B = load_schedule_from_csv("schedule_B.csv", "同学B")
    
    # 合并课表
    all_schedules = schedule_A + schedule_B
    
    # 需求1：输出文本视图
    print_schedule_view(all_schedules)
    
    # 需求2：计算每个人的空闲时间
    print_all_free_times(all_schedules)

if __name__ == "__main__":
    main()