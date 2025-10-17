from typing import List, Dict, Optional

def average_salary_by_department(data: List[dict], min_salary: Optional[int] = None) -> Dict[str, float]:

    totals: dict[str, int] = {}
    counts: dict[str, int] = {}

    for emp in data:
        sal = emp.get("salary")
        dept = emp.get("department")
        if sal is None or dept is None:
            continue
        if min_salary is not None and sal < min_salary:
            continue
        totals[dept] = totals.get(dept, 0) + sal
        counts[dept] = counts.get(dept, 0) + 1

    result: dict[str, float] = {}
    for dept, total in totals.items():
        cnt = counts[dept]
        if cnt == 0:
            continue
        avg = total / cnt
        result[dept] = int(avg) if avg == int(avg) else avg

    return result


if __name__ == "__main__":
    employees = [
        {"name": "Aarav", "salary": 120000, "department": "Engineering"},
        {"name": "Sita", "salary": 90000, "department": "Marketing"},
        {"name": "Kiran", "salary": 130000, "department": "Engineering"},
        {"name": "Mina", "salary": 95000, "department": "Finance"},
    ]
    print(average_salary_by_department(employees))
    print(average_salary_by_department(employees, min_salary=100000))
 
