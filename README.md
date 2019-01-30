# audio-prep
audio-prep is a module developed to segment meaningful-spoken part of an audio signal

## Installation

```console
$ pip install -r requirements.txt
```

## How to use

### Example

```Python
sample_rate, processed_signal = PreProcessing().process(file_name='robot-5.wav', combine=False, threshold=0.01)
```

## Example result

### Original signal

<img src="https://user-images.githubusercontent.com/22976651/51966991-b6197600-24a0-11e9-9a1b-edb52b725843.png" width="400" height="280">

### Processed signal without signal combination
<img src="https://user-images.githubusercontent.com/22976651/51967411-d564d300-24a1-11e9-9902-240db5b81ff9.png" width="400" height="280">

### Original signal with signal combination
<img src="https://user-images.githubusercontent.com/22976651/51967434-e0b7fe80-24a1-11e9-96fe-0b14b3a14451.png" width="400" height="280">
