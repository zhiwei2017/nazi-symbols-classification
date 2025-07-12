nazi-symbols-classification
===========================

Introduction
------------
Nazi symbols classification source code.

User Guide
----------

How to Install
++++++++++++++

Stable release
``````````````

To install nazi-symbols-classification, run this command in your terminal:

.. code-block:: console

    $ pip install nazi_symbols_classification

or

.. code-block:: console

    $ poetry self add nazi_symbols_classification

This is the preferred method to install nazi-symbols-classification, as it will always install the most recent stable release.


From sources
````````````

The sources for nazi-symbols-classification can be downloaded from the `Github repo <https://github.com/zhiwei2017/nazi-symbols-classification>`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone https://github.com/zhiwei2017/nazi-symbols-classification.git

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ pip install .

or

.. code-block:: console

    $ poetry install

How to Use
++++++++++

nazi-symbols-classification
```````````````````````````

To use nazi-symbols-classification in a project::

    import nazi_symbols_classification

nazi_symbols_classification_backend
```````````````````````````````````

To run the `nazi_symbols_classification_backend` locally with docker compose::

    $  docker compose run --service-ports nazi_symbols_classification_backend

The docker image for `nazi_symbols_classification_backend` is published in DockerHub
repository `nazi-symbols-classification-backend <https://hub.docker.com/repository/docker/chasingcars/nazi-symbols-classification-backend/general>`_.
You can pull it with::

    docker push chasingcars/nazi-symbols-classification-backend:latest

Send Image to predict
`````````````````````

Assuming that the `nazi_symbols_classification_backend` is running at `http://localhost:8080` and the
paths of images to be sent are `["dummy_folder/image_1.jpg", "dummy_folder/image_2.png"]`.

To send images to the endpoint `http://localhost:8080/api/v1/predict`, you can do it with python::

    import requests

    extension_to_content_type = {
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png"
    }

    def classify_document(file_paths, api_endpoint):
        files = []
        for file_path in file_paths:
            extension = file_path.split(".")[-1].lower()
            content_type = extension_to_content_type[extension]
            files.append(("images", (file_path, open(file_path, 'rb'), content_type)))
        response = requests.post(api_endpoint,
                                 files=files,
                                 timeout=10)
        response.raise_for_status()
        result = response.json()
        return result

    classify_document(["dummy_folder/image_1.jpg", "dummy_folder/image_2.png"],
                       "http://localhost:8080/api/v1/predict")

or with curl::

    curl -X 'POST' \
      'http://localhost:8080/api/v1/predict' \
      -H 'accept: application/json' \
      -H 'Content-Type: multipart/form-data' \
      -F 'images=@dummy_folder/image_1.jpg;type=image/jpeg'
      -F 'images=@dummy_folder/image_2.png;type=image/png'

How to run notebooks
++++++++++++++++++++

To run the notebooks, you need to have `nb` group dependencies installed. You can install them with::

    $ poetry install --with nb

You can start Jupyter Notebook with the following command::

    $ jupyter notebook


After that, you can run the notebooks in the `notebooks` folder using Jupyter Notebook or JupyterLab. For
details on how to use the notebooks and what they contain, please refer to the
`README.md <https://github.com/zhiwei2017/nazi-symbols-classification/tree/develop/notebooks/README.md>`_
in `notebooks` folder.


Maintainers
-----------

..
    TODO: List here the people responsible for the development and maintaining of this project.
    Format: **Name** - *Role/Responsibility* - Email

* **Zhiwei Zhang** - *Maintainer* - `zhiwei2017@gmail.com <mailto:zhiwei2017@gmail.com?subject=[GitHub]nazi-symbols-classification>`_