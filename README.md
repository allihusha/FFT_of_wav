# FFT of WAV

Проект для передачи аудио по UDP с последующим БПФ анализом и фильтрацией шума через DeepFilterNet.

## Требования

- Python 3.12 (DeepFilterNet не поддерживает версии выше)
- Rust (для сборки DeepFilterNet)

## Установка (macOS)

```
python3.12 -m venv .venv
```

```
source .venv/bin/activate
```

```
pip install numpy matplotlib torch==2.6.0 torchaudio==2.6.0
```

```
pip install git+https://github.com/Rikorose/DeepFilterNet.git#subdirectory=pyDF
```

```
pip install git+https://github.com/Rikorose/DeepFilterNet.git#subdirectory=DeepFilterNet
```

## Установка (Windows)

```
python -m venv .venv
```

```
.venv\Scripts\activate
```

```
pip install numpy matplotlib torch==2.6.0 torchaudio==2.6.0
```

```
pip install git+https://github.com/Rikorose/DeepFilterNet.git#subdirectory=pyDF
```

```
pip install git+https://github.com/Rikorose/DeepFilterNet.git#subdirectory=DeepFilterNet
```

DeepFilterNet устанавливается с GitHub, а не через `pip install deepfilternet`, потому что версия на PyPI (0.5.6) содержит устаревший импорт который был убран в новых версиях torchaudio. Версия с GitHub (0.5.7rc0) содержит исправление этой проблемы.
