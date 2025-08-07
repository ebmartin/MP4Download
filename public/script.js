document.getElementById('download-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('url').value;
    const message = document.getElementById('message');

    message.textContent = 'Procesando tu solicitud... por favor espera.';
    message.style.color = '#007bff';

    try {
        const response = await fetch('/.netlify/functions/download', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url })
        });

        if (response.ok) {
            const blob = await response.blob();
            const downloadUrl = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = downloadUrl;
            const contentDisposition = response.headers.get('Content-Disposition');
            let filename = 'video.mp4'; // --- CAMBIO AQUÍ ---
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="(.+)"/);
                if (filenameMatch && filenameMatch.length > 1) {
                    filename = filenameMatch[1];
                }
            }
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            a.remove();
            message.textContent = 'Descarga iniciada.';
            message.style.color = 'green';
        } else {
            const errorText = await response.text();
            message.textContent = `Error: ${errorText || 'Ocurrió un error inesperado.'}`;
            message.style.color = 'red';
        }
    } catch (error) {
        message.textContent = `Error de conexión: ${error.message}`;
        message.style.color = 'red';
        console.error('Error:', error);
    }
});
