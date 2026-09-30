# 需求3：查找共同空闲时间并排序
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

def print_all_free_times(people_list, schedule_list, day_start="08:00", day_end="22:00"):
    """打印每个人的空闲时间段"""
    print("===== 【所有人的空闲时间段】 =====")
    day_start_min = time_to_minutes(day_start)
    day_end_min = time_to_minutes(day_end)
    days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    for person in people_list:
        print(f"--- {person} 的空闲时间 ---")
        person_schedule = [c for c in schedule_list if c['person'] == person]
        for day in days:
            slots = get_person_free_slots(person_schedule, day, day_start_min, day_end_min)
            if slots:
                slot_strs = [f"{minutes_to_time(s)} - {minutes_to_time(e)}" for s, e in slots]
                print(f"[{day}] 空闲: {', '.join(slot_strs)}")
    print("===============================\n")

# ================= 需求3：找共同空闲时间 =================
def find_common_free_times(people_list, all_schedules, day_start="08:00", day_end="22:00"):
    """找所有人的共同空闲时间，并按空闲时长排序（超长超赞）"""
    print("===== 【所有人共有的空闲时间段】 =====")
    day_start_min = time_to_minutes(day_start)
    day_end_min = time_to_minutes(day_end)
    days = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"]
    
    for day in days:
        # 提取每个人当天的空闲时间
        all_free_slots = []
        for person in people_list:
            person_schedule = [c for c in all_schedules if c['person'] == person]
            slots = get_person_free_slots(person_schedule, day, day_start_min, day_end_min)
            if not slots:
                all_free_slots = [] 
                break
            all_free_slots.append(slots)
        
        if not all_free_slots:
            print(f"[{day}] 无共同空闲时间")
            continue
        
        # 求交集 (两个两个求交集)
        common_slots = all_free_slots[0]
        for i in range(1, len(all_free_slots)):
            new_common = []
            for c_start, c_end in common_slots:
                for p_start, p_end in all_free_slots[i]:
                    overlap_start = max(c_start, p_start)
                    overlap_end = min(c_end, p_end)
                    # 共同空闲也要大于30分钟
                    if overlap_end - overlap_start >= 30:
                        new_common.append((overlap_start, overlap_end))
            common_slots = new_common
        
        # 按空闲时长从大到小排序（超长超赞排序）
        common_slots.sort(key=lambda x: x[1] - x[0], reverse=True)
        
        # 输出
        result_strs = [f"{minutes_to_time(s)} - {minutes_to_time(e)} ({e-s}分钟)" for s, e in common_slots]
        print(f"[{day}] 共同空闲: {', '.join(result_strs) if result_strs else '无'}")
    print("===============================\n")

# ================= 主程序 =================
def main():
    print("欢迎使用课表解析工具！")
    
    # 显式定义所有人的名单（这步极其重要，防止某人没课时被忽略）
    people_list = ["同学A", "同学B"]
    
    # 读取多个人的课表
    schedule_A = load_schedule_from_csv("schedule.csv", "同学A")
    schedule_B = load_schedule_from_csv("schedule_B.csv", "同学B")
    
    # 合并课表
    all_schedules = schedule_A + schedule_B
    
    # 需求1：输出文本视图
    print_schedule_view(all_schedules)
    
    # 需求2：计算每个人的空闲时间
    print_all_free_times(people_list, all_schedules)
    
    # 需求3：计算共同空闲时间
    find_common_free_times(people_list, all_schedules)

if __name__ == "__main__":
    main()