# Key Pressed

Aplicacion de escritorio para mantener presionadas hasta 10 teclas mientras juegas.

## Requisitos

- Windows 10/11
- Python 3.10 o superior

## Instalacion y ejecucion

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Selecciona las teclas en la ventana y usa `Ctrl+F12` para mantenerlas presionadas. Usa `Ctrl+F10` para soltarlas y deshabilitar la app. Tambien puedes usar los botones de la ventana.

Al cerrar la aplicacion, las teclas sostenidas se liberan. Si el juego se ejecuta como administrador y no recibe las teclas, ejecuta tambien esta aplicacion como administrador.