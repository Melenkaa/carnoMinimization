import itertools
import pandas as pd


def get_minterms(df, output_var):
    """Возвращает список минтермов для заданной выходной переменной."""
    minterms = []
    for _, row in df.iterrows():
        if row[output_var] == 1:
            minterms.append(tuple(row[:-11]))  # Берем только входные переменные
    return minterms


def minimize_boolean_function(minterms, variables):
    """Выполняет минимизацию булевой функции по карте Карно."""
    if not minterms:
        return "0"

    terms = set(minterms)
    while True:
        new_terms = set()
        used = set()
        for t1, t2 in itertools.combinations(terms, 2):
            diff = [i for i in range(len(t1)) if t1[i] != t2[i]]
            if len(diff) == 1:
                new_term = list(t1)
                new_term[diff[0]] = '-'
                new_terms.add(tuple(new_term))
                used.add(t1)
                used.add(t2)

        terms -= used
        terms |= new_terms

        if not new_terms:
            break

    simplified_exprs = []
    for term in terms:
        expr_parts = []
        for i, val in enumerate(term):
            if val == 1:
                expr_parts.append(variables[i])
            elif val == 0:
                expr_parts.append(f"!{variables[i]}")
        simplified_exprs.append(" & ".join(expr_parts))

    return " | ".join(simplified_exprs)


# Загрузка данных из файла
file_path = "ITable.xlsx"
xls = pd.ExcelFile(file_path)
df = xls.parse(sheet_name='Sheet1')

# Переименовываем столбцы для удобства
df.columns = ['a', 'b', 'c', 'q1', 'q2', 'q3', 'q4', '_', 'i1', 'i2', 'i3', 'i4', 'i5', 'i6', 'i7', 'i8', 'i9', 'i10',
              'i11']
df = df.drop(columns=['_'])  # Удаляем ненужный столбец

# Определяем входные переменные
variables = ['a', 'b', 'c', 'q1', 'q2', 'q3', 'q4']

# Минимизируем каждую функцию
minimized_expressions = {
    f'i{i + 1}': minimize_boolean_function(get_minterms(df, f'i{i + 1}'), variables) for i in range(11)
}

# Выводим минимизированные выражения
for key, expr in minimized_expressions.items():
    print(f"{key}: {expr}")
