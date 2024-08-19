from rx import create
from rx.core import Observer
from rx import of, operators

class Printer(Observer):
    def on_next(self, v):
        print(f'Recibido: {v}')
        
    def on_completed(self):
        print("Fin")
            
def generator(observer, scheduler):
    observer.on_next("Hola")
    observer.on_next("Adios")
    observer.on_completed()
    
observable = create(generator)

printer = Printer()
# observable.subscribe(on_next=lambda v: print(f'Recibido: {v}'))
observable.subscribe(printer)

def observable_teclado(observer, scheduler):
    while 1:
        msg = input('Introduzca un mensaje: ')
        if msg:
            observer.on_next(msg)
        else:
            observer.on_completed()
            return
observable = create(observable_teclado)
observable.subscribe(printer)


observable = of("Hola", "Adios")

observable2 = observable.pipe(
    operators.map(lambda s: s.upper()),
    operators.map(lambda s: f'En mayusculas: {s}')
    
).subscribe(Printer())

# Se puede poner de esta manera o poniendo .subscribe(Printer()) despues del cierre del pipe
#printer = Printer()
#observable2.subscribe(printer)