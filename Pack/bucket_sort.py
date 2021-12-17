
import json
from tqdm import tqdm


def insertion_sort(bucket: list):
    for i in range(1, len(bucket)):
        var = bucket[i]['weight']
        j = i - 1
        v = bucket[j]['weight']
        while j >= 0 and var < v:
            bucket[j + 1] = bucket[j]
            j = j - 1
        bucket[j + 1] = bucket[i]


# В функцию сортировки требуется: список (словарей) и параметр, по которому происходит сортировка
def bucket_sort(data: list, value: str):
    """
    Самое большое значение в списке – max_value. Размер списка – len(data).
    Используя эти 2 значения, выясним оптимальный size для каждого сегмента: делим max элемент на len списка.
    Теперь при делении значения элемента на size, мы получаем  индекс для каждого сегмента соответствующего элемента.
    """
    max_value = 0
    for i in range(len(data)):
        if int(data[i][value]) > max_value:
            max_value = data[i][value]
    size = max_value / len(data)
    """
    Создадим столько же блоков, сколько и элементов в списке.
    """
    buckets_list = []
    for x in range(len(data)):
        buckets_list.append([])
    with tqdm(data, desc="Сортируем") as pbar:
        """
         Помещаем элементы списка в разные блоки на основе size.
        """
        for i in range(len(data)):
            j = int(data[i][value] / size)
            if j != len(data):
                buckets_list[j].append(data[i])
            else:
                buckets_list[len(data) - 1].append(data[i])
            pbar.update(1)
    """
    Сортируем элементы внутри блоков с помощью сортировки вставкой.
    """
    for z in range(len(data)):
        insertion_sort(buckets_list[z])


    """
    Объединяем блоки с отсортированными элементами в один список
    """
    final_output = []
    for x in range(len(data)):
        final_output += buckets_list[x]
    return final_output


def read_file(file_input: str):
    with open(file_input, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data


def save_file(file_output: str, data: list):
    with open(file_output, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
