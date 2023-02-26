import datetime
import requests

from utils.handler import Handlers


def get_jaeger_analysis_data():
    trace_url = "http://172.16.23.231:30531/api/v1/service-proxy/cluster/dev/namespace/observability/service/jaeger-query/port/16686/api/traces"
    param = {
        # "end": 1662611631714000,
        "limit": 100,
        "lookback": "1h",
        "service": "smartvoice-dmkit",
        # "start": 1662608031714000
    }

    res = requests.request(method="GET", url=trace_url, params=param, verify=False)
    data_list = res.json()["data"]
    all_data = []
    for data in data_list:
        trace_info = {"traceID": data["traceID"]}
        for info in data["spans"]:
            trace_info[info["operationName"]] = info["duration"]
        all_data.append(trace_info)

    if 1 == 1:
        filename = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        Handlers.write_list_map_as_excel(list_map=all_data, excel_writer=filename + ".xlsx",
                                         sheet_name="Sheet1", index=False)


if __name__ == '__main__':
    get_jaeger_analysis_data()
