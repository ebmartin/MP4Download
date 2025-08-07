import json
import base64
import os
from pytube import YouTube
from tempfile import TemporaryDirectory
import os

def handler(event, context):
    """
    Función de Netlify para descargar un video de YouTube.
    """
    try:
        body = json.loads(event['body'])
        video_url = body.get('url')

        if not video_url:
            return {
                'statusCode': 400,
                'body': 'URL de YouTube no proporcionada.'
            }

        with TemporaryDirectory() as temp_dir:
            yt = YouTube(video_url)
            
            # --- CAMBIO CLAVE AQUÍ ---
            # En lugar de solo audio, obtenemos el stream de mayor resolución con video y audio
            stream = yt.streams.get_highest_resolution()
            
            if not stream:
                return {
                    'statusCode': 404,
                    'body': 'No se encontró un stream de alta resolución para el video.'
                }

            file_path = stream.download(output_path=temp_dir)
            
            # El nombre del archivo ahora termina en .mp4
            filename = yt.title + '.mp4'

            with open(file_path, 'rb') as f:
                file_content = f.read()
                encoded_file = base64.b64encode(file_content).decode('utf-8')
            
            # El Content-Type ahora es para un video MP4
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'video/mp4',
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
