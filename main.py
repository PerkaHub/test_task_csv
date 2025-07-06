import argparse
import csv
import sys

from tabulate import tabulate


OPERATORS = ["<", ">", "="]


class CSVHandler:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = self.read_csv()
        self.aggregation_result = None

    def read_csv(self):
        with open(self.file_path, mode="r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return list(reader)

    def aggregate(self, aggregate_func):
        if not aggregate_func:
            return self

        try:
            column, func = aggregate_func.split("=")
            values = [float(row[column]) for row in self.data if row[column]]

            if func == "min":
                result = min(values) if values else 0
            elif func == "max":
                result = max(values) if values else 0
            elif func == "avg":
                result = sum(values) / len(values) if values else 0
            else:
                raise ValueError((f'Неизвестная агрегатная функция {func}'))

            self.aggregation_result = [func, result]
        except ValueError:
            raise
        except Exception as e:
            print(f"Ошибка агрегации {e}")

        return self

    def filtration(self, where):
        if not where:
            return self
        try:
            for op in OPERATORS:
                if op in where:
                    column, operator, value = where.partition(op)
                    break
            filtered = []
            for row in self.data:
                if operator == "=" and str(row[column]) == value:
                    filtered.append(row)
                elif operator == "<" and float(row[column]) < float(value):
                    filtered.append(row)
                elif operator == ">" and float(row[column]) > float(value):
                    filtered.append(row)

            self.data = filtered
        except Exception as e:
            print(f"Ошибка фильтрации {e}")
            sys.exit(1)

        return self

    def print_results(self):
        if not self.data and not self.aggregation_result:
            print("Нет данных")
            return

        if self.aggregation_result:
            print(
                tabulate(
                    [[self.aggregation_result[0]], [self.aggregation_result[1]]],
                    tablefmt="grid",
                )
            )
            return
        headers = self.data[0].keys()
        rows = [row.values() for row in self.data]
        print(tabulate(rows, headers=headers, tablefmt="grid"))


def main():
    parser = argparse.ArgumentParser(description="Filtration and agregation")
    parser.add_argument("--file", type=str, help="Path to input file")
    parser.add_argument("--aggregate", type=str, help="Agregate function")
    parser.add_argument("--where", type=str, help="Filter function")
    args = parser.parse_args()

    Core = CSVHandler(args.file)
    Core.aggregate(args.aggregate).filtration(args.where).print_results()


if __name__ == "__main__":
    main()
