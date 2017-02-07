# Speech recognition app

This is an example of a speech recognition app.
The application `speech_recognition_app.py` uses the Python package
`SpeechRecognition` and processes the data either offline (using `SPHINX`)
or online (using Google's Speech API).
It also saves the recording as a `wav` file.

The `printer.py` just prints the output value.

## Installing dependencies
- `portaudio19-dev`, `python3-all-dev` and `swig`:
```shell
sudo apt install portaudio19-dev python3-all-dev swig
```
- Python packages:
```shell
sudo pip3 install --upgrade pip SpeechRecognition pyaudio setuptools wheel pocketsphinx
```

## Usage
```shell
pAntler speech_recognition.moos
```
