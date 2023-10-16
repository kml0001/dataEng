import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import json


def json_to_parquet(json_file, schema, parquet_file):
    # Cargar el JSON en un DataFrame de Pandas
    with open(json_file, 'r') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    # Validar el esquema
    if not validate_schema(df, schema):
        raise ValueError("El JSON no cumple con el esquema proporcionado.")

    # Convertir tipos de datos especiales antes de convertir el DataFrame de Pandas a una tabla Arrow
    for col, dtype in schema.items():
        if dtype == "boolean":
            df[col] = df[col].astype(bool)
        elif dtype == "date":
            df[col] = pd.to_datetime(df[col])

    # Convertir el DataFrame de Pandas a una tabla Arrow
    table = pa.Table.from_pandas(df)

    # Escribir la tabla Arrow en un archivo Parquet
    with open(parquet_file, 'wb') as f:
        pq.write_table(table, f)


def validate_schema(df, schema):
    # Implementa la lógica de validación de esquema aquí
    # Puedes comparar el esquema del DataFrame con el esquema proporcionado
    # y asegurarte de que coincidan según tus requisitos

    # Por ejemplo, puedes verificar que todas las columnas requeridas estén presentes
    # y que los tipos de datos coincidan con el esquema proporcionado.

    # Retorna True si el esquema es válido, False en caso contrario.
    return True


# Uso del método
json_file_path = '../projects/flattened_projects.json'
schema = {
    "id": "int",
    "name": "string",
    "identifier": "string",
    "description": "string",
    "status": "int",
    "is_public": "boolean",
    "inherit_members": "boolean",
    "created_on": "date",
    "updated_on": "date"
}
parquet_file = 'datos.parquet'

json_to_parquet(json_file_path, schema, parquet_file)
