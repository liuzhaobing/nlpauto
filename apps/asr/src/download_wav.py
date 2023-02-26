import requests

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
    url = "http://172.16.23.83:30515/roc/quoto/cdmCo"
    payload = {
        "[]": {
            "dwm_svo_anno_label_event_i_d": {
                "question_id{}": question_ids,
                "@column": "question_id,rcu_audio"
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
    question_ids_list, info = get_question_ids(file_path=r"C:\Users\liuzhaobing\Desktop\asr.xlsx", sheet_name="Sheet2")
    results = big_data(question_ids=question_ids_list)
    path = r"D:\\workspace\\"
    test_cases = []
    for case in results:
        question_id = case["dwm_svo_anno_label_event_i_d"]["question_id"]
        rcu_audio = case["dwm_svo_anno_label_event_i_d"]["rcu_audio"]
        text = info[question_id]
        filename = path + text + "__" + question_id + ".wav"
        try:
            download_file(url=rcu_audio, file_name=filename)
            test_cases.append({
                "question_text": text,
                "wav_filename": filename,
                "question_id": question_id
            })
        except Exception as e:
            print(e)
            continue
    Handlers.write_list_map_as_excel(test_cases, excel_writer=f"{path}asr_cases.xlsx", sheet_name="Sheet1", index=False)
