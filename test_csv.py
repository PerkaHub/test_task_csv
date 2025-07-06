import pytest

from main import CSVHandler


def test_read_csv():
    handler = CSVHandler('products_test.csv')
    assert len(handler.data) == 4
    assert handler.data[0]['name'] == 'iphone 15'


def test_aggregation_max():
    handler = CSVHandler('products_test.csv')
    handler.aggregate('price=max')
    assert handler.aggregation_result == ['max', 1200]


def test_aggregation_min():
    handler = CSVHandler('products_test.csv')
    handler.aggregate('price=min')
    assert handler.aggregation_result == ['min', 300]


def test_aggregation_avg():
    handler = CSVHandler('products_test.csv')
    handler.aggregate('price=avg')
    assert handler.aggregation_result == ['avg', 874.75]


def test_invalid_aggregation_func():
    handler = CSVHandler('products_test.csv')
    with pytest.raises(ValueError, match='Неизвестная агрегатная функция'):
        handler.aggregate('price=unknown')


def test_filtration_equal():
    handler = CSVHandler('products_test.csv')
    handler.filtration('brand=apple')
    assert handler.data[0]['brand'] == 'apple'


def test_filtration_less():
    handler = CSVHandler('products_test.csv')
    handler.filtration('price<400')
    assert handler.data[0]['brand'] == 'xiaomi'


def test_filtration_more():
    handler = CSVHandler('products_test.csv')
    handler.filtration('price>1000')
    assert handler.data[0]['brand'] == 'xiaomi'


def test_filtration_invalid_operator():
    handler = CSVHandler('products_test.csv')
    with pytest.raises(SystemExit):
        handler.filtration('price!=1000')


def test_print_aggregation_results(capsys):
    handler = CSVHandler('products_test.csv')
    handler.aggregate('price=avg')
    handler.print_results()
    captured = capsys.readouterr()
    assert "avg" in captured.out
    assert str(874.75) in captured.out


def test_print_filtered_results(capsys):
    handler = CSVHandler('products_test.csv')
    handler.filtration('brand=apple')
    handler.print_results()
    captured = capsys.readouterr()
    assert 'apple' in captured.out
    assert 'sumsung' not in captured.out


def test_print_filtered_empty_results(capsys):
    handler = CSVHandler('products_test.csv')
    handler.filtration('brand=honor')
    handler.print_results()
    captured = capsys.readouterr()
    assert 'Нет данных' in captured.out
