import json
import boto3
import uuid
import os

def lambda_handler(event, context):
    try:
        # 1. Log INFO de inicio (opcional pero recomendado)
        log_inicio = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Iniciando ejecución de lambda_handler",
                "evento_recibido": event # Grabamos el evento original
            }
        }
        print(json.dumps(log_inicio))

        # Extracción de datos
        # Asumiendo que el body llega como un diccionario. Si llega como string, usa json.loads()
        body = event.get('body', {})
        if isinstance(body, str):
            body = json.loads(body)

        tenant_id = body['tenant_id']
        pelicula_datos = body['pelicula_datos']
        nombre_tabla = os.environ["TABLE_NAME"]

        # Proceso
        uuidv4 = str(uuid.uuid4())
        pelicula = {
            'tenant_id': tenant_id,
            'uuid': uuidv4,
            'pelicula_datos': pelicula_datos
        }
        
        # Guardar en DynamoDB
        dynamodb = boto3.resource('dynamodb')
        table = dynamodb.Table(nombre_tabla)
        response = table.put_item(Item=pelicula)

        # 2. Log INFO de éxito (Estandarizado)
        log_exito = {
            "tipo": "INFO",
            "log_datos": {
                "mensaje": "Película creada y guardada exitosamente",
                "pelicula": pelicula
            }
        }
        print(json.dumps(log_exito))

        # Salida
        return {
            'statusCode': 200,
            'body': json.dumps({
                'mensaje': 'Éxito',
                'pelicula': pelicula
            })
        }

    except Exception as e:
        # 3. Manejo de Errores: Log ERROR (Estandarizado)
        log_error = {
            "tipo": "ERROR",
            "log_datos": {
                "mensaje": "Ocurrió un error durante la ejecución del Lambda",
                "detalle_error": str(e)
            }
        }
        print(json.dumps(log_error))
        
        # Retornamos un error 500 al cliente en lugar de un colapso total
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Error interno del servidor',
                'detalle': str(e)
            })
        }