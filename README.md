---
title: Deep Barcode Reader
emoji: 🔳
colorFrom: gray
colorTo: red
sdk: streamlit
sdk_version: 1.42.2
app_file: app.py
pinned: false
---
# Deep-Barcode-Reader
This repository is used for reading different types of barcodes and QR codes from images.
The code is written in Python and uses OpenCV, Pyzbar, and other libraries for reading barcodes and QR codes.


## How to Use
The library offers several functions for reading barcodes and QR codes from images.
General options can be selected before applying the reader method. These options are:
- `--data_path` is the path to the image file.
- `--result_path` is the path to the output file.
- `--verbose` is the verbosity level of the code.
- `--method` is the method for reading the barcode or QR code.
- `--model_size` is the size of the deep learning model.

The available methods are as:
- [Opencv Barcode Reader](#opencv-barcode-reader)
- [Zbar Barcode Reader](#zbar-barcode-reader)
- [QR Reader](#qr-reader)

### Opencv Barcode Reader
This method can only detect barcodes but NOT QR codes. It can detect and decode EAN-8, EAN-13, UPC-A and UPC-E
barcode types. You can use the method by running the following command:
```shell
deep_barcode_reader -vv -d tests/test_data/sample.jpg -m opencv
```
This method can only detect specific types of barcodes. However, it is faster than the other methods.

### Zbar Barcode Reader
This method can detect and decode both barcodes and QR codes.
It is very powerful to detect and decode different types of barcodes and QR codes.
You can use the method by running the following command:
```shell
deep_barcode_reader -vv -d tests/test_data/sample.jpg -m zbar
```

### QR Reader
This method can only detect and decode QR codes.
Depending on the model size as `n` as nano, `s` as small, `m` as medium, or `l` as large,
the detection and decoding process time and accuracy can be changed.
```shell
deep_barcode_reader -vv -d tests/test_data/sample.jpg -m zbar --model_size l
```


## How to Develop
Do the following only once after creating your project:
- Init the git repo with `git init`.
- Add files with `git add .`.
- Then `git commit -m 'initialize the project'`.
- Add remote url with `git remote add origin REPO_URL`.
- Then `git branch -M master`.
- `git push origin main`.
Then create a branch with `git checkout -b BRANCH_NAME` for further developments.
- Install poetry if you do not have it in your system from [here](https://python-poetry.org/docs/#installing-with-pipx).
- Create a virtual env preferably with virtualenv wrapper and `mkvirtualenv -p $(which python3.10) ENVNAME`.
- Then `git add poetry.lock`.
- Then `pre-commit install`.
- For applying changes use `pre-commit run --all-files`.


## Docker Container
To run the docker with ssh, do the following first and then based on your need select ,test, development, or production containers:
```shell
export DOCKER_BUILDKIT=1
export DOCKER_SSHAGENT="-v $SSH_AUTH_SOCK:$SSH_AUTH_SOCK -e SSH_AUTH_SOCK"
```
### Test Container
This container is used for testing purposes while it runs the test
```shell
docker build --progress plain --ssh default --target test -t barcode_docker:test .
docker run -it --rm -v "$(pwd):/app" $(echo $DOCKER_SSHAGENT) barcode_docker:test
```

### Development Container
This container can be used for development purposes:
```shell
docker build --progress plain --ssh default --target development -t barcode_docker:development .
docker run -it --rm -v "$(pwd):/app" -v /tmp:/tmp $(echo $DOCKER_SSHAGENT) barcode_docker:development
```

### Production Container
This container can be used for production purposes:
```shell
docker build --progress plain --ssh default --target production -t barcode_docker:production .
docker run -it --rm -v "$(pwd):/app" -v /tmp:/tmp $(echo $DOCKER_SSHAGENT) barcode_docker:production deep_barcode_reader -vv -d tests/test_data/sample.jpg -m zbar --model_size l
```

## Hugging Face Deployment
The repository is also deployed in [hugging face](https://huggingface.co/spaces/afshin-dini/Deep-Barcode-Reader) in which one can upload images, select the appropriate method and its parameters and detect and decode the barcodes or QR codes.
It is good to mention that you can also run the application locally by running the following command:
```shell
streamlit run app.py
```
and then open the browser and go to the address `http://localhost:8501`.
