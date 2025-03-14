def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report)


def ensure_report_valid(report):
    res = True
    if not isinstance(report, bytes):
        res = False
        print("report not bytes")
    if len(report) != 8:
        res = False
        print("report too long")
    if report[1] != 0:
        print("report[1] not 0")
        res = False
    return res


class PlainReportApplier:
    def __init__(self):
        pass

    def apply(self, report):
        if ensure_report_valid(report):
            write_report(report)
