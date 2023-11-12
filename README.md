# Unzipper

Unzipper è uno script in Python che monitora la cartella dei download per estrarre automaticamente gli archivi compressi, spostandoli nel cestino dopo l'estrazione.

## Installazione

1. **Clone il repository:**
   ```
   git clone https://github.com/tuoutro/Unzipper.git
2. **Crea e attiva un ambiente virtuale (venv):**
    ```
    cd Unzipper
    python -m venv venv
### Per sistemi operativi basati su Unix
    source venv/bin/activate  
### Per Windows
    .\venv\Scripts\activate
3. **Installa le dipendenze:**
    ```
    pip install -r requirements.txt
4. **Esegui lo script:**
    ```
    python main.py
## Opzioni avanzate
Se stai usando PyInstaller per creare un eseguibile, puoi includere manualmente le dipendenze aggiuntive con il seguente comando:

```
pyinstaller --onefile --hidden-import=patoolib.programs.p7zip --hidden-import=patoolib.programs.rar --hidden-import=Send2Trash --hidden-import=watchdog --noconsole main.py
```
Questa istruzione crea un eseguibile senza finestra del prompt dei comandi e include le dipendenze necessarie per l'estrazione di archivi 7z e RAR.

## Contribuisci
Se trovi bug o hai miglioramenti da suggerire, sentiti libero di aprire una nuova issue o inviare una pull request.

Grazie per l'utilizzo di Unzipper!