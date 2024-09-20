import csv
from people.models import Person

from pathlib import Path

def populate_database(csv_file_path:Path, batch_size:int) -> bool:
    if Person.objects.exists():
        Person.objects.all().delete()

    try:
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            person_objects = []

            for i, row in enumerate(reader):
                person_objects.append(Person(
                    codigo=row['Codigo'],
                    apellidos_y_nombres=row['Apellidos y Nombres'],
                    carrera_primera_opcion=row['Carrera Primera Opción'],
                    puntaje= 0.0 if not row['Puntaje'] else float(row['Puntaje']),
                    merito=row['Merito'],
                    observacion=row.get('Observación', None),
                    carrera_segunda_opcion=row.get('Carrera Segunda Opción', None),
                    fecha=row['Fecha'],
                    modalidad_de_ingreso=row['Modalidad de ingreso']
                ))

                # Insert in batches
                if len(person_objects) >= batch_size:
                    Person.objects.bulk_create(person_objects)
                    person_objects = []  # Clear the list for the next batch
            
            # Insert any remaining objects not in a full batch
            if person_objects:
                Person.objects.bulk_create(person_objects)
    except Exception as e:
        print(f"Error populating database: {e}")
        Person.objects.all().delete()
        return False
    else:
        return True

     