def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report)


class PlainReportApplier:
    def __init__(self):
        pass

    def apply(self, data):
        write_report(data)