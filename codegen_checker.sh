#!/usr/bin/env bash
# Скрипт для генерации моделей SQLAlchemy по существующей БД
#
# Если модели уже существуют, делает diff с новыми моделями и выводит разницу
# в отдельный файл

# Пусть до файла с моделями, с которым будем сравнивать
# Например, ./exported_models/models.py
PATH_TO_EXIST_MODELS=${1}

# Путь до БД, откуда будем генерировать модели
# Например, firebird://SYSDBA:isc_admin@localhost:3050//firebird/data/expedition_merman
PATH_TO_DB=${2}

# Директория, куда будем складывать результаты диффов
PATH_TO_DIFFERS_DIRECTORY=${3}

TEMP_FILE_NAME="models.py"

PATH_TO_TEMP_FILE=${PATH_TO_DIFFERS_DIRECTORY}/${TEMP_FILE_NAME}

if [[ ! -f "$PATH_TO_EXIST_MODELS" ]]
then
    # Генерируем новые модели, если их нет
    sqlacodegen ${PATH_TO_DB} > ${PATH_TO_EXIST_MODELS}

    if [[ "$?" -ne "0" ]]; then
      echo "Не удалось сгенерировать модели"
      exit 1
    fi

    echo "ok"
else
    # Создаем директорию, где будем хранить результаты диффов
    if [[ ! -d "$PATH_TO_DIFFERS_DIRECTORY" ]]
    then
        mkdir ${PATH_TO_DIFFERS_DIRECTORY}
    fi

    # Удаляем временный файл с моделями
    if [[ -f ${PATH_TO_TEMP_FILE} ]]
    then
        rm -f ${PATH_TO_TEMP_FILE}
    fi

    # Генерируем новые модели
    sqlacodegen ${PATH_TO_DB} > ${PATH_TO_TEMP_FILE}

    if [[ "$?" -ne "0" ]]; then
      echo "Не удалось сгенерировать модели"
      exit 1
    fi

    current_date=$(date -u +%Y-%m-%d-%T-%Z)
    diff_result_file=${PATH_TO_DIFFERS_DIRECTORY}/diff_${current_date}.txt

    diff -u ${PATH_TO_EXIST_MODELS} ${PATH_TO_TEMP_FILE} > ${diff_result_file}

    if [[ -s "$diff_result_file" ]]
    then
        echo "*****АХТУНГ!******"
        echo "Файлы отличаются. Смотри "${diff_result_file}
        echo "*******************"
    else
        echo "Файлы совпадают"
        echo "Файлы идентичны" > ${diff_result_file}
    fi
fi