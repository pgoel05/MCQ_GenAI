import os
import PyPDF2
import json
import traceback
import pandas as pd


def readFile(fileName: str):
    """Read data from the file

    Args:
        fileName (str): File name containing data

    Returns:
        data (str): Text
    """

    if fileName.name.endswith(".pdf"):
        try:
            pdf = PyPDF2.PdfFileReader(fileName)
            data = ""

            for page in pdf.pages:
                data += page.extract_text()

            return data
        except Exception as e:
            raise Exception("error reading the pdf file")

    elif fileName.name.endswith(".txt"):
        return fileName.read().decode("utf-8")

    else:
        raise Exception("Unsupported file format")


def formatData(quiz: str):
    """Converts quiz string into a DataFrame

    Args:
        quiz (str): quiz as a string

    Returns:
        quiz (df): quiz as a DataFrame
    """
    quiz_table_data = []
    for key, value in quiz.items():
        mcq = value["mcq"]
        options = " | ".join(
            [
                f"{option}: {option_value}"
                for option, option_value in value["options"].items()
            ]
        )
        correct = value["correct"]
        quiz_table_data.append({"MCQ": mcq, "Choices": options, "Correct": correct})

    return pd.DataFrame(quiz_table_data)
