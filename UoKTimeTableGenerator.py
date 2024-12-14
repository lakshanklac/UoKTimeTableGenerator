# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 18:10:14 2024

@author: K.L.A.C. LAKSHAN
"""


def schedule_classes(courses, conflicts, room_capacities, course_sizes, teachers, repetitions):
    """
    Schedule courses considering repetitions, time slots, room capacities, teacher availability,
    daily uniqueness, and student priorities.
    
    Args:
    courses (list): List of course names.
    conflicts (dict): Adjacency list representing course conflicts.
    room_capacities (list): List of room capacities.
    course_sizes (dict): Number of students for each course.
    teachers (dict): Mapping of courses to their assigned teachers.
    repetitions (dict): Number of days each course must repeat in a week.
    
    Returns:
    dict: Schedule with course, room, and teacher assignments.
    """
    # Initialize schedule: {day: {timeslot: {room: (course, teacher)}}}
    schedule = {day: {} for day in range(5)}  # Monday to Friday
    teacher_availability = {teacher: {day: set() for day in range(5)} for teacher in set(teachers.values())}

    # Sort courses by the number of students (priority for larger classes)
    sorted_courses = sorted(courses, key=lambda x: course_sizes[x], reverse=True)

    for course in sorted_courses:
        days_assigned = 0
        teacher = teachers[course]
        assigned_days = set()

        while days_assigned < repetitions[course]:
            for day in range(5):
                if day in assigned_days:
                    continue

                for timeslot in range(len(room_capacities)):
                    # Check if the teacher is available
                    if timeslot in teacher_availability[teacher][day]:
                        continue

                    # Ensure the same course doesn't appear twice on the same day
                    if course in [
                        data[0] for timeslot_rooms in schedule[day].values() for data in timeslot_rooms.values()
                    ]:
                        continue

                    for room_index, room_capacity in enumerate(room_capacities):
                        # Check if the room is available and can fit the course
                        if room_index not in schedule[day].get(timeslot, {}) and room_capacity >= course_sizes[course]:
                            # Check for conflicts in the same timeslot
                            if all(conflicted not in [
                                data[0] for data in schedule[day].get(timeslot, {}).values()
                            ] for conflicted in conflicts[course]):
                                # Assign course to this room, timeslot, and day
                                if timeslot not in schedule[day]:
                                    schedule[day][timeslot] = {}
                                schedule[day][timeslot][room_index] = (course, teacher)
                                teacher_availability[teacher][day].add(timeslot)
                                assigned_days.add(day)
                                days_assigned += 1
                                break
                    if days_assigned == repetitions[course]:
                        break
                if days_assigned == repetitions[course]:
                    break

    return schedule


# Input: Courses, Conflicts, Room Capacities, Course Sizes, Teachers, and Repetitions
courses = ['Math', 'Physics', 'Chemistry', 'Biology', 'Computer Science', 'Statistics', 'Electronics']
conflicts = {
    'Math': ['Physics', 'Chemistry'],
    'Physics': ['Math', 'Biology', 'Electronics'],
    'Chemistry': ['Math', 'Biology'],
    'Biology': ['Physics', 'Chemistry'],
    'Computer Science': [],
    'Statistics': [],
    'Electronics': ['Physics']
}
room_capacities = [50, 40, 20]  # R1, R2, R3
course_sizes = {
    'Math': 20,
    'Physics': 20,
    'Chemistry': 30,
    'Biology': 30,
    'Computer Science': 40,
    'Statistics': 40,
    'Electronics': 40
}
teachers = {
    'Math': 'Mr A',
    'Physics': 'Mr A',
    'Chemistry': 'Mr B',
    'Biology': 'Mr B',
    'Computer Science': 'Mr C',
    'Statistics': 'Mr D',
    'Electronics': 'Mr E'
}
repetitions = {
    'Math': 5,
    'Physics': 4,
    'Chemistry': 1,
    'Biology': 1,
    'Computer Science': 3,
    'Statistics': 1,
    'Electronics': 1
}

# Generate Timetable
timetable = schedule_classes(courses, conflicts, room_capacities, course_sizes, teachers, repetitions)

# Format and Print Timetable Day by Day
days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
print("Course Timetable (Day-wise Schedule):")
for day_index, day in enumerate(days):
    print(f"\n{day}:")
    for timeslot in range(len(room_capacities)):
        if timeslot in timetable[day_index]:
            for room, (course, teacher) in timetable[day_index][timeslot].items():
                print(f"  Timeslot {timeslot + 1}: {course} (Room: R{room + 1}, Teacher: {teacher})")
        else:
            print(f"  Timeslot {timeslot + 1}: No Class")
