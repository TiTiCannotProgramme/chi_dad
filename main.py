import pandas as pd
from typing import List, Dict


def get_duplications(input_list: List[float]) -> Dict[float, int]:
    result_dict: Dict[float, int] = {}
    for value in input_list:
        if value in result_dict:
            result_dict[value] += 1
        else:
            result_dict[value] = 1
    result_dict = {key: value for (key, value) in result_dict.items() if value > 1}
    return result_dict


def list_to_look_up_table(input_list: List[float]) -> Dict[float, int]:
    result_dict: Dict[float, int] = {}

    sorted_list: List[float] = sorted(input_list)

    for idx, value in enumerate(sorted_list):
        if value in result_dict:
            result_dict[value] += 1
        else:
            result_dict[value] = idx

    return result_dict


def list_to_look_up_table_2(input_list: List[float]) -> Dict[float, int]:
    result_dict: Dict[float, int] = {}

    sorted_list: List[float] = sorted(input_list)

    for idx, value in enumerate(sorted_list):
        if value in result_dict:
            # result_dict[value] += 1
            pass
        else:
            result_dict[value] = idx

    return result_dict


def find_possible_labels(
        features: Dict[str, float],
        labels_positions_look_up: Dict[str, Dict[float, int]]
) -> List[str]:
    label_position: Dict[str, int] = {}

    for label, feature_value in features.items():
        feature_position_look_up: Dict[float, int] = labels_positions_look_up[label]
        label_position[label] = feature_position_look_up[feature_value]
    # print(label_position)
    return get_labels_by(label_position)


def get_labels_by(label_position: Dict[str, int]) -> List[str]:
    max_position: int = 0
    for _, position in label_position.items():
        if position > max_position:
            max_position = position

    result: List[str] = []
    for label, position in label_position.items():
        if position == max_position:
            result.append(label)

    return result


if __name__ == "__main__":
    df = pd.read_stata("./data/data_tianrui.dta")

    labels: List[str] = list(df.columns)[1:6]

    labels_positions_look_up: Dict[str, Dict[float, int]] = {}
    labels_positions_look_up_2: Dict[str, Dict[float, int]] = {}

    for label in labels:
        feature_values: List[float] = list(df[label])
        labels_positions_look_up[label] = list_to_look_up_table(feature_values)
        labels_positions_look_up_2[label] = list_to_look_up_table_2(feature_values)
        print(label)
        print(get_duplications(feature_values))

    keys_to_remove: List[str] = ["year", "id"]
    max_labels: List[List[str]] = []
    max_labels_2: List[List[str]] = []
    for index, row in df.iterrows():
        feature_dict: Dict[str, float] = row.to_dict()

        for key in keys_to_remove:
            feature_dict.pop(key, None)

        result_labels: List[str] = find_possible_labels(feature_dict, labels_positions_look_up)
        result_labels_2: List[str] = find_possible_labels(feature_dict, labels_positions_look_up_2)
        max_labels.append(result_labels)
        max_labels_2.append(result_labels_2)

    # difference: int = 0
    # for i in range(len(max_labels)):
    #     if max_labels[i] != max_labels_2[i]:
    #         difference += 1
    # print(difference)

    # for key, value in labels_positions_look_up.items():
    #     print(len(value))
    # #
    # # print(df.duplicated(labels).sum())
    # print(df.shape)
    # duplicated_values: int = 0
    # for labels in max_labels_2:
    #     if len(labels) > 1:
    #         duplicated_values += 1
    # print(duplicated_values)
