import json
import base64
import os
from pytube import YouTube
from tempfile import TemporaryDirectory
import os

def handler(event, context):
    """
    Función de Netlify para descargar audio de YouTube.
    """
    try:
        # Analiza el cuerpo de la solicitud JSON
        body = json.loads(event['body'])
        video_url = body.get('url')

        if not video_url:
            return {
                'statusCode': 400,
                'body': 'URL de YouTube no proporcionada.'
            }

        # Descarga el audio en un directorio temporal
        with TemporaryDirectory() as temp_dir:
            yt = YouTube(video_url)
            stream = yt.streams.filter(only_audio=True).first()
            if not stream:
                return {
                    'statusCode': 404,
                    'body': 'No se encontró un stream de audio para el video.'
                }

            file_path = stream.download(output_path=temp_dir)
            
            # Obtiene el nombre del archivo del stream
            filename = yt.title + '.m4a'
            # Lee el archivo en memoria y lo codifica en Base64
            with open(file_path, 'rb') as f:
                file_content = f.read()
                encoded_file = base64.b64encode(file_content).decode('utf-8')
            
            # Configura la respuesta para la descarga
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'audio/m4a',
                    'Content-Disposition': f'attachment; filename="{filename}"',
                },
                'body': encoded_file,
                'isBase64Encoded': True
            }

    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }