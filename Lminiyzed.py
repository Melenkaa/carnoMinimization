import itertools
import pandas as pd


def get_minterms(df, output_var, input_vars):
    """Возвращает список минтермов для заданной выходной переменной."""
    minterms = []
    for _, row in df.iterrows():
        if row[output_var] == 1:
            minterms.append(tuple(row[input_vars]))  # Берем только входные переменные
    return minterms


def minimize_boolean_function(minterms, variables):
    """Выполняет минимизацию булевой функции по карте Карно."""
    if not minterms:
        return "0"  # Если нет минтермов, то функция равна 0

    terms = set(minterms)
    while True:
        new_terms = set()
        used = set()
        for t1, t2 in itertools.combinations(terms, 2):
            diff = [i for i in range(len(t1)) if t1[i] != t2[i]]
            if len(diff) == 1:  # Различие в одной переменной, можно объединить
                new_term = list(t1)
                new_term[diff[0]] = '-'
                new_terms.add(tuple(new_term))
                used.add(t1)
                used.add(t2)

        terms -= used
        terms |= new_terms

        if not new_terms:
            break

    # Преобразуем импликанты в логические выражения
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
file_path = "/home/kevgen/Documents/Lминимизация Андрея.xlsx"
xls = pd.ExcelFile(file_path)
df = xls.parse(sheet_name='Sheet1')

# Переименовываем столбцы для удобства
df.columns = ['q1', 'q2', 'q3', 'q4', '_', 'L1', 'L2', 'L3', 'L4', 'L5', 'L6', 'L7', 'L8', 'L9', 'L10', 'L11']
df = df.drop(columns=['_'])  # Удаляем ненужный столбец

# Определяем входные переменные
input_vars = ['q1', 'q2', 'q3', 'q4']
output_vars = [f'L{i}' for i in range(1, 12)]

# Минимизируем каждую функцию
minimized_expressions = {
    output_var: minimize_boolean_function(get_minterms(df, output_var, input_vars), input_vars)
    for output_var in output_vars
}

# Выводим минимизированные выражения
for key, expr in minimized_expressions.items():
    print(f"{key}: {expr}")