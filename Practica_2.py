import tkinter as tk
from tkinter import ttk
import asyncio
from PIL import Image, ImageTk
import aiohttp
from bs4 import BeautifulSoup
from io import BytesIO
from rx.scheduler.eventloop import AsyncIOScheduler
from rx import create
import threading

class AsyncImageDownloader:
    # Inicializador de la clase: Configura la ventana principal y las variables iniciales.
    def __init__(self, root, loop):
        self.root = root  # La ventana principal de la aplicación.
        self.loop = loop  # El bucle de eventos para operaciones asíncronas.
        self.init_ui()  # Llama a la función para construir la interfaz de usuario.
        self.image_objects = {}  # Diccionario para almacenar las imágenes descargadas.
        self.scheduler = AsyncIOScheduler(loop=loop)  # Scheduler para ReactiveX con asyncio.
        self.disposable = None  # Objeto para manejar la cancelación de suscripciones Rx.

    # Configura la interfaz de usuario utilizando el administrador de geometría 'grid'.
    def init_ui(self):
        # Configura las filas y columnas de la ventana principal.
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
        for i in range(2):
            self.root.grid_columnconfigure(i, weight=1)

        # Crea y coloca los widgets de la interfaz de usuario.
        url_label = tk.Label(self.root, text="URL a procesar")
        url_label.grid(row=0, column=0, sticky="ew")

        self.url_entry = tk.Entry(self.root)
        self.url_entry.grid(row=0, column=1, sticky="ew")

        self.search_button = tk.Button(self.root, text="Buscar", command=self.start_download)
        self.search_button.grid(row=0, column=2, sticky="ew")

        self.listbox = tk.Listbox(self.root)
        self.listbox.grid(row=1, column=0, sticky="ns")

        self.image_label = tk.Label(self.root)
        self.image_label.grid(row=1, column=1, rowspan=2, sticky="nsew")

        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.grid(row=2, column=0, sticky="ew")

        self.status_label = tk.Label(self.root, text="")
        self.status_label.grid(row=3, column=0, sticky="ew")

        self.listbox.bind('<<ListboxSelect>>', self.on_image_select)

    # Función asincrónica para descargar imágenes de una URL.
    def image_downloader(self, observer, scheduler, url):
        async def download_images(url):
            # Inicia una sesión HTTP asincrónica.
            async with aiohttp.ClientSession() as session:
                # Realiza una solicitud GET a la URL.
                async with session.get(url) as response:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    images = soup.find_all('img')
                    self.progress["maximum"] = len(images)
                    for index, img in enumerate(images):
                        img_url = img.get('src')
                        # Descarga los datos de la imagen.
                        async with session.get(img_url) as img_response:
                            img_data = await img_response.read()
                            image = Image.open(BytesIO(img_data))
                            photo = ImageTk.PhotoImage(image)
                            self.image_objects[img_url] = photo  # Almacena la referencia de la imagen.
                            observer.on_next((img_url, photo))  # Notifica al observer.
                            self.root.after(0, self.update_progress, index + 1)  # Actualiza la barra de progreso.
            observer.on_completed()  # Notifica al observer que la descarga está completa.

        # Ejecuta la tarea asincrónica en el bucle de eventos de asyncio.
        asyncio.run_coroutine_threadsafe(download_images(url), loop)

    # Se llama cuando el usuario hace clic en el botón "Buscar".
    def start_download(self):
        # Obtiene la URL de la entrada y crea un observable para la descarga de imágenes.
        url = self.url_entry.get()
        self.observable = create(lambda obs, sch: self.image_downloader(obs, sch, url))
        # Cancela cualquier descarga anterior y suscribe a la nueva.
        if self.disposable:
            self.disposable.dispose()
        self.disposable = self.observable.subscribe(
            on_next=lambda item: self.root.after(0, self.update_ui, item),
            on_error=lambda e: print(f"Error: {e}"),
            on_completed=lambda: print("Download completed"),
            scheduler=self.scheduler)

    # Maneja la selección de elementos en la Listbox.
    def on_image_select(self, event):
        self.root.update_idletasks()  # Procesa eventos pendientes para asegurarse de que la selección se ha actualizado.
        widget = event.widget
        selection = widget.curselection()
        if selection:
            index = int(selection[0])
            img_url = widget.get(index)
            photo_image = self.image_objects.get(img_url)
            if photo_image:
                self.image_label.configure(image=photo_image)  # Actualiza la imagen mostrada.
                self.image_label.image = photo_image  # Mantiene la referencia a la imagen.
            else:
                print("Imagen no encontrada en el objeto de imagen.")
        else:
            print("No hay ninguna imagen seleccionada.")

    # Actualiza la interfaz de usuario cuando se descarga una nueva imagen.
    def update_ui(self, item):
        img_url, photo = item
        self.listbox.insert(tk.END, img_url)
        self.status_label.configure(text=f"Se han encontrado {self.listbox.size()} imágenes")

    # Actualiza la barra de progreso a medida que se descargan las imágenes.
    def update_progress(self, value):
        self.progress['value'] = value
        self.progress.update_idletasks()
        if value >= self.progress["maximum"]:
            self.status_label.configure(text=f"Todas las imágenes han sido descargadas. Total: {self.progress['maximum']}")

def observe_images(app, scheduler):
    def on_next(item):
        app.update_ui(item)
    
    def on_subscribe(observer, _):
        # Esto asocia el observer con la función on_next
        observer.on_next = on_next

    return create(on_subscribe).subscribe(scheduler=scheduler)

def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    root = tk.Tk()
    app = AsyncImageDownloader(root, loop)

    # Ejecuta el bucle de eventos en un nuevo hilo
    threading.Thread(target=run_asyncio_loop, args=(loop,), daemon=True).start()

    root.mainloop()

    # Asegúrate de detener el bucle de eventos después de cerrar la ventana de Tkinter
    loop.call_soon_threadsafe(loop.stop)
    threading.Thread(target=loop.close).start()