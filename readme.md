## Description
Test suites for working with the shopping cart and filtering products for the site https://tehnomaks.ru/

## Usage
### Install dependencies
```shell
pip install -r requirements.txt
```

### Move to 'test_cart_and_filters' directory
```shell
cd .\test_cart_and_filters\
```

### Run

#### Positive Cart tests

```shell
pytest -svvv tests.py::TestCartPositive
```

#### Negative Cart tests

```shell
pytest -svvv tests.py::TestCartNegative
```

#### Filters tests

```shell
pytest -svvv tests.py::TestFilters
```


