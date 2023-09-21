# python-library

This is the python boilerplate i use in nearly all python projects i use.

## design

* tornado for an HTTP framework
* can be installed via pip
* runs in docker
* can create a python wheel
* allows for local development
* sane logging defaults
* standard python library best practices
* debugging info on /debugz
* since its using tornado you can easily do async and multithreading easily

### tornado
tornado is a mature http framework with lots of coding examples
everywhere and really good [documentation](https://www.tornadoweb.org/en/branch6.3/).

sure [Fast API](https://fastapi.tiangolo.com/) is similar in speed comparisons and you can use that too
but I chose to use tornado.

## renaming python_library

```console
git clone git@github.com:armanye/python-library.git
find python-library -type f -exec \
    sed -i -e 's/python-library/your-library/g' \
           -e 's/python_library/your_library/g' {} \;
```
make sure to rename everything in the commands below.

## local development

### via docker

Both options allow you to develop locally and the server automatically
updates.

```console
cd docker
docker compose up --build app
```

### via python
```console
python3 -m venv /tmp/venv
source /tmp/venv/bin/activate
python3 setup.py develop
python3 -m python_library
```

### links
* [http://127.0.0.1:1234/debugz](http://127.0.0.1:1234/debugz) - Show
  some debugging info.  Way more useful with the [json formatter chrome
  extension](https://chrome.google.com/webstore/detail/json-formatter/bcjindcccaagfpapjjmafapmmgkkhgoa?hl=en)

## deploy

### make a wheel file
```console
pip install wheel
python3 setup.py bdist_wheel
ls dist/*.whl
```
