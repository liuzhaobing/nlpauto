# -*- coding:utf-8 -*-
import requests
import subprocess

from utils.handler import Handlers


def get_question_ids(file_path, sheet_name):
    question_ids = []
    info = {}
    result = Handlers.read_excel_as_list_map(io=file_path, sheet_name=sheet_name)
    for r in result:
        question_ids.append(r["question_id"])
        info[r["question_id"]] = r["question_text"]
    return question_ids, info


def big_data(question_ids):
    url = "http://kubernetes-prod-3.cloudminds.com:30515/data/quoto/cdmCo"
    payload = {
        "[]": {
            "dwm_svo_anno_label_event_i_d": {
                "question_id{}": question_ids,
                "@column": "question_id,rcu_audio,question_text"
            },
            "page": 0,
            "count": len(question_ids)
        }
    }
    headers = {
        "cookie": "JSESSIONID=D3CC5F43BB153197A45A69696429B1AE",
        "Content-Type": "application/json",
        "token": "UUNWAX0Z2APUBZYJ9S1F"
    }
    response = requests.request("POST", url, json=payload, headers=headers)
    return response.json()['[]']


def download_file(url, file_name):
    r = requests.get(url, stream=True)
    with open(file_name, 'wb') as f:
        for ch in r:
            f.write(ch)
    f.close()


if __name__ == '__main__':
    question_ids_list, info = get_question_ids(file_path=r"./data/asr自动化测试-李森.xlsx", sheet_name="原始数据")
    results = big_data(question_ids=question_ids_list)
    path = ""
    test_cases = []

    for case in results:
        question_id = case["dwm_svo_anno_label_event_i_d"]["question_id"]
        rcu_audio = case["dwm_svo_anno_label_event_i_d"]["rcu_audio"]
        text = info[question_id]
        filename = path + text + "__" + question_id + ".wav"
        rcu_audio.replace("&", "\&")
        result = subprocess.run(f"wget {rcu_audio} -O {filename}", shell=True, capture_output=True, text=True)
        error = result.stderr
        output = result.stdout

    Handlers.write_list_map_as_excel(test_cases, excel_writer=f"{path}asr_cases.xlsx", sheet_name="Sheet1", index=False)
