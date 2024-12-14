# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 18:10:14 2024

@author: K.L.A.C. LAKSHAN
"""

def schedule_classes(courses, conflicts, room_capacities, course_sizes, teachers, repetitions, pre_assignments):
    """
    Schedule courses considering repetitions, pre-assigned classes, time slots, room capacities,
    teacher availability, daily uniqueness, and student priorities.
    
    Args:
    courses (list): List of course names.
    conflicts (dict): Adjacency list representing course conflicts.
    room_capacities (list): List of room capacities.
    course_sizes (dict): Number of students for each course.
    teachers (dict): Mapping of courses to their assigned teachers.
    repetitions (dict): Number of days each course must repeat in a week.
    pre_assignments (dict): Pre-assigned classes with format {course: (day, timeslot, room)}.
    
    Returns:
    dict: Schedule with course, room, and teacher assignments.
    """
    # Initialize schedule: {day: {timeslot: {room: (course, teacher)}}}
    schedule = {day: {} for day in range(5)}  # Monday to Friday
    teacher_availability = {teacher: {day: set() for day in range(5)} for teacher in set(teachers.values())}

    # Handle pre-assignments first
    for course, (day, timeslot, room) in pre_assignments.items():
        teacher = teachers[course]
        if repetitions[course] > 0:
            if day not in schedule:
                schedule[day] = {}
            if timeslot not in schedule[day]:
                schedule[day][timeslot] = {}
            schedule[day][timeslot][room] = (course, teacher)
            teacher_availability[teacher][day].add(timeslot)
            repetitions[course] -= 1  # Reduce repetitions for pre-assigned courses

    # Sort remaining courses by the number of repetitions (priority for higher repetitions)
    sorted_courses = sorted(courses, key=lambda x: repetitions[x], reverse=True)

    for course in sorted_courses:
        teacher = teachers[course]
        while repetitions[course] > 0:
            for day in range(5):  # Loop through weekdays
                for timeslot in range(len(room_capacities)):
                    # Skip if teacher is unavailable at this timeslot
                    if timeslot in teacher_availability[teacher][day]:
                        continue

                    # Skip if the course is already scheduled on the same day
                    if course in [data[0] for slot in schedule[day].values() for data in slot.values()]:
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
                                repetitions[course] -= 1  # Reduce repetitions for the course
                                break
                    if repetitions[course] == 0:
                        break
                if repetitions[course] == 0:
                    break

    return schedule


# Input: Courses, Conflicts, Room Capacities, Course Sizes, Teachers, Repetitions, and Pre-Assignments
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
pre_assignments = {
    'Math': (0, 0, 0),  # Math is pre-set to be on Monday, Timeslot 1, Room R1
    'Physics': (1, 1, 0)  # Physics is pre-set to be on Tuesday, Timeslot 2, Room R1
}

# Generate Timetable
timetable = schedule_classes(courses, conflicts, room_capacities, course_sizes, teachers, repetitions, pre_assignments)

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
