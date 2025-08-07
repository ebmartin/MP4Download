import json

def handler(event, context):
    return {
        'statusCode': 200,
        'body': json.dumps('¡Hola mundo! La función de Python funciona.')
    }
