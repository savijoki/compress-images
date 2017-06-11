# About

This repository contains a small python script for image compression using [Pillow](https://github.com/python-pillow/Pillow), which is a fork of Python Imaging Library (PIL). Both PNG and JPEG -filetypes are supported. Filetype is recognized using [python-magic](https://github.com/ahupp/python-magic).

The script supports Python versions 3.3, 3.4, 3.5 and 3.6.

## Setup

Create virtual environment:
```bash
$ virtualenv venv -p python3
```
Activate virtual environment:
```bash
$ source venv/bin/activate
```
Install requirements:
```bash
$ pip install -r requirements.txt
```

## Usage

```bash
$ python3 main.py <path-to-directory>
```
