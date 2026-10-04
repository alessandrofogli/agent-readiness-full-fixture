from worker.jobs import nightly_digest


class _FakeQuery:
    def all(self):
        return [1, 2, 3]


class _FakeSession:
    def query(self, _model):
        return _FakeQuery()


def test_nightly_digest_uses_flag() -> None:
    result = nightly_digest(_FakeSession())
    # beta_dashboard default is False -> job reports itself skipped
    assert result == {"skipped": True, "reason": "beta_dashboard disabled"}
