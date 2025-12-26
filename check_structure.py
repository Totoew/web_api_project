import os
import sys

# Структура проекта
expected_structure = {
    'app': {
        '__init__.py': None,
        'main.py': None,
        'config.py': None,
        'database.py': None,
        'models': {
            '__init__.py': None,
            'repo_event.py': None
        },
        'schemas': {
            '__init__.py': None,
            'repo_event.py': None
        },
        'api': {
            '__init__.py': None,
            'dependencies.py': None,
            'routers.py': None,
            'endpoints': {
                '__init__.py': None,
                'events.py': None,
                'tasks.py': None
            }
        },
        'services': {
            '__init__.py': None,
            'github_service.py': None,
            'event_service.py': None,
            'nats_service.py': None
        },
        'tasks': {
            '__init__.py': None,
            'background.py': None
        },
        'websocket': {
            '__init__.py': None,
            'ws_manager.py': None
        },
        'nats': {
            '__init__.py': None,
            'publisher.py': None,
            'subscriber.py': None
        }
    }
}

def check_directory(base_path, structure):
    """Рекурсивно проверяем структуру директорий и файлов"""
    missing = []
    
    for item, substructure in structure.items():
        item_path = os.path.join(base_path, item)
        
        if isinstance(substructure, dict):
            # Это директория
            if not os.path.exists(item_path):
                missing.append(f"❌ Отсутствует директория: {item_path}")
            elif not os.path.isdir(item_path):
                missing.append(f"❌ {item_path} не является директорией")
            else:
                # Рекурсивно проверяем вложенную структуру
                missing.extend(check_directory(item_path, substructure))
        else:
            # Это файл
            if not os.path.exists(item_path):
                missing.append(f"❌ Отсутствует файл: {item_path}")
            elif not os.path.isfile(item_path):
                missing.append(f"❌ {item_path} не является файлом")
    
    return missing

print("Проверка структуры проекта...")
print("=" * 50)

# Текущая директория
base_dir = os.path.dirname(os.path.abspath(__file__))

# Проверяем корневые файлы
root_files = ['requirements.txt', 'README.md', 'docker-compose.yml', 'Dockerfile']
for file in root_files:
    file_path = os.path.join(base_dir, file)
    if os.path.exists(file_path):
        print(f"✅ {file}")
    else:
        print(f"❌ Отсутствует: {file}")

print("\nПроверка структуры app/ директории:")
print("-" * 50)

missing_files = check_directory(os.path.join(base_dir, 'app'), expected_structure['app'])

if missing_files:
    print("\nПроблемы найдены:")
    for msg in missing_files:
        print(msg)
else:
    print("✅ Все файлы и директории на месте!")

# Проверяем наличие пустых __init__.py файлов
print("\nПроверка __init__.py файлов:")
print("-" * 50)

init_files = [
    'app/__init__.py',
    'app/models/__init__.py',
    'app/schemas/__init__.py',
    'app/api/__init__.py',
    'app/api/endpoints/__init__.py',
    'app/services/__init__.py',
    'app/tasks/__init__.py',
    'app/websocket/__init__.py',
    'app/nats/__init__.py'
]

for init_file in init_files:
    file_path = os.path.join(base_dir, init_file)
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            content = f.read().strip()
            if content:
                print(f"✅ {init_file} (не пустой)")
            else:
                print(f"⚠️  {init_file} (пустой, но это нормально)")
    else:
        print(f"❌ Отсутствует: {init_file}")

print("\n" + "=" * 50)
print("Проверка завершена!")