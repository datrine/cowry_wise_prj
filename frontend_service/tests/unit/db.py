


class DBConnectionMock:
    def __init__(self):
        self.recorder = Recorder()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_value, exc_tb):
        return self
    
    def fake_init_db(self):
        self.recorder.called = True
        print("teardown")
#    result = runner.invoke(args=['init-db'])
#    assert 'Initialized' in result.output
#    assert Recorder.called

class Recorder(object):
    called = False


