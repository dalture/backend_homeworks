from enum import Enum

# не уверена, что status и остальные классы про важность/срочность именно тут стоит хранить
class TaskStatus(str, Enum): 
    new = 'new'
    in_progress = 'in progress'
    done = 'done'
    late = 'late'
    cancelled = 'cancelled'

# класс важностей задач
class TaskImportance(str, Enum): 
    low = 'low'
    medium = 'medium'
    high = 'high'

# класс срочностей задач
class TaskUrgency(str, Enum): 
    low = 'low'
    medium = 'medium'
    high = 'high'