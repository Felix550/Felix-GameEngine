## English Version
[English Version](readme_eng.md)

# Felix Game Engine - User Lua API

## • Types

### `Color(r, g, b, a=1)`
Rappresenta un colore RGBA.
- **r**: componente rossa (0–255)
- **g**: componente verde (0–255)
- **b**: componente blu (0–255)
- **a**: alfa (0–1)

### `Vector2D(x, y)`
Rappresenta un vettore bidimensionale.
- **x**: coordinata X
- **y**: coordinata Y

#### Funzioni:
- `Vector2D.add(Vector2D || int || float)` → aggiunge un valore al Vector2D
- `Vector2D.sub(Vector2D || int || float)` → sottrae un valore al Vector2D

### `ShapeType`
Definisce la forma di un attore.
- `RECTANGLE`: rettangolo
- `ELLIPSE`: cerchio / ellisse
- `SPRITE`: sprite (non ancora implementato)
- `LINE`: linea
- `ARC`: arco
- `TEXT`: testo

### `Align`
Definisce l'allineamento del disegno.
- `CENTER`: centra la forma nel punto specificato
- `CORNER`: disegna dal vertice superiore sinistro

### `TextAlign`
Definisce l'allineamento del disegno.
- `LEFT`: allinea il testo a sinistra in alto
- `CENTER`: allinea il testo al centro in mezzo
- `RIGHT`: allinea il testo a destra in alto

### `KeyCode`
Definisce una lista di Tasti per tastiera.
- `K_`: Cominciano per K_

### `MouseButton`
Definisce i Bottoni per il Mouse.
- `LEFT`: Tasto Sinistro.
- `MIDDLE`: Tasto Centrale.
- `RIGHT`: Tasto Destro.

---

## • Objects

### `Actor(position, shape_type, data)`
Crea un oggetto disegnabile.
- **position**: `Vector2D` posizione dell’attore
- **shape_type**: tipo della forma (`ShapeType`)
- **data**: dizionario delle proprietà (Vedi `Shape Data`)

#### Funzioni:
- `Actor.move(deltaPosition)` → sposta l’attore
- `Actor.set_pos(newPosition)` → imposta la posizione assoluta
- `Actor.get_pos()` → ottiene la posizione assoluta
- `Actor.change_data(key, value)` → modifica una proprietà nel dizionario `data`
- `Actor.get_data(key)` → ottiene una proprietà nel dizionario `data`
- `Actor.get_size()` → ottiene la dimensione del testo renderizzato (Usato solo se ShapeType è TEXT)
- `Actor.colliding(Actor)` → restituisce Vero se 2 `Actor` collidono

---

### `Font(fontName, fontSize, bold (false), italic (false))`
Crea un oggetto disegnabile.
- **fontName**: nome del Font di Sistema
- **fontSize**: dimensione del font
- **bold**: il testo è in grassetto se Vero
- **italic**: il testo è in italico se Vero

---

### `Canvas`
Rappresenta la superficie su cui disegnare.

#### Funzioni:
- `Canvas.fill(color)` → riempie lo schermo con un colore
- `Canvas.draw(actor)` → disegna un attore (`Actor`)

---

### `Window`
Gestisce le proprietà della finestra.

#### Funzioni:
- `Window.set_title(title)` → imposta il titolo della finestra
- `Window.get_title()` → restituisce il titolo attuale
- `Window.set_size(Vector2D)` → imposta la dimensione della finestra
- `Window.get_size()` → restituisce la dimensione (`Vector2D`)
- `Window.set_target_fps(fps)` → imposta il framerate desiderato
- `Window.get_target_fps()` → restituisce il framerate impostato
- `Window.toggle_fullscreen()` → scorre tra Fullscreen e Windowed
- `Window.show_console()` → mostra la console
- `Window.hide_console()` → nasconde la console
- `Window.set_icon(path)` → imposta l'icona della finestra con un percorso relativo alla cartella assets
  
### `Screen`
Gestisce le proprietà dello schermo.

#### Funzioni:
- `Screen.get_size()` → restituisce la risoluzione dello schermo fisico

---

### `Mouse`
Gestisce il mouse.

#### Funzioni:
- `Mouse.get_pos()` → restituisce la posizione (`Vector2D`)
- `Mouse.set_pos(Vector2D)` → imposta la posizione del cursore
- `Mouse.GetButton(MouseButton)` → restituisce Vero se il bottone è costantemente premuto
- `Mouse.GetButtonDown(MouseButton)` → restituisce Vero se il bottone è stato premuto
- `Mouse.GetButtonUp(MouseButton)` → restituisce Vero se il bottone è stato lasciato

### `Input`
Gestisce gli input.

#### Funzioni:
- `Input.GetKey(KeyCode)` → restituisce Vero se la Key è costantemente premuta
- `Input.GetKeyDown(KeyCode)` → restituisce Vero se la Key è stata premuta
- `Input.GetKeyUp(KeyCode)` → restituisce Vero se la Key è stata lasciata

---

### `Debug`
Sistema di logging basilare.

#### Funzioni:
- `Debug.log(text)` → stampa un messaggio con timestamp
- `Debug.get_entry_file()` → ottiene il perscorso assoluto del file .lua principale
- `Debug.get_assets_folder()` → ottiene il perscorso assoluto della cartella assets

---

## • Shape Data

### `RECTANGLE`
Un Rettangolo (o Quadrato).

#### Propietà in Data:
- **size**: `Vector2D` dimensione Rettangolo
- **color**: `Color` colore Rettangolo
- **align**: `Align` allineamento pivot Rettangolo

---

### `ELLIPSE`
Un'Ellisse (o Cerchio).

#### Propietà in Data:
- **size**: `Vector2D` dimensione Ellisse
- **color**: `Color` colore Ellisse
- **align**: `Align` allineamento pivot Ellise

---

### `SPRITE`
Un'Immagine.

#### Propietà in Data:
- **path**: percorso relativo alla asset folder
- **size**: `Vector2D` dimensione Immagine
- **align**: `Align` allineamento pivot Immagine
- **alpha**: se vero renderizzerà l'immagine tagliando via il layer Alpha (trasparente)

---

### `LINE`
Una Linea.

#### Propietà:
##### Ce bisogno di specificare che in una linea il parametro posizionale è usato come serie di 2 punti:

`Vector2D(Vector2D(x1,y1),Vector2D(x2,y2))`

#### Propietà in Data:
- **color**: `Color` colore Linea
- **width**: spessore Linea

### `ARC`
Un'Arco.

#### Propietà in Data:
- **size**: `Vector2D` dimensione Arco
- **color**: `Color` colore Arco
- **start_angle**: angolo di partenza Arco
- **stop_angle**: angolo di fine Arco
- **width**: spessore Arco

---

### `TEXT`
Un'Arco.

#### Propietà in Data:
- **text**: Testo
- **color**: `Color` colore del Testo
- **font**: `Font` font usato dal Testo
- **text_align**: `TextAlign` allineamento del Testo
- **antialias**: se Vero userà la tecnica di Antialiasing

---

## • Funzioni globali

### `wait(seconds: float)`
Sospende l’esecuzione (thread Engine) per il numero di secondi specificato.

---

## • Funzioni principali Lua

### `On_Start()`
Richiamata una volta all’avvio dello script.

### `On_Runtime(deltaTime: float, fps: float, frame: int)`
Richiamata ogni frame.
- **deltaTime**: tempo trascorso dal frame precedente (in secondi)
- **fps**: framerate corrente
- **frame**: indice del frame corrente

### `On_KeyDown(key: KeyCode)`
Richiamata quando una Key è stata premuta.
- **key**: Key premuta

### `On_KeyUp(key: KeyCode)`
Richiamata quando una Key è stata lasciata.
- **key**: Key lasciata
