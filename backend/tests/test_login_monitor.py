from app.services.login_monitor import LoginMonitor


def test_lockout_starts_after_five_failed_attempts():
    monitor = LoginMonitor()

    for _ in range(4):
        monitor.record_failure("student@example.com")

    assert monitor.is_locked("student@example.com") is False

    monitor.record_failure("student@example.com")

    assert monitor.is_locked("student@example.com") is True


def test_lockout_has_remaining_time():
    monitor = LoginMonitor(lockout_minutes=15)

    for _ in range(5):
        monitor.record_failure("student@example.com")

    remaining = monitor.remaining_lockout_seconds("student@example.com")

    assert 0 < remaining <= 900


def test_attempts_during_lockout_do_not_extend_it():
    monitor = LoginMonitor(lockout_minutes=15)

    for _ in range(5):
        monitor.record_failure("student@example.com")

    original_expiry = monitor._states[
        "student@example.com"
    ].locked_until

    monitor.record_failure("student@example.com")

    new_expiry = monitor._states[
        "student@example.com"
    ].locked_until

    assert new_expiry == original_expiry
    assert monitor.is_locked("student@example.com") is True


def test_successful_login_clears_failure_history():
    monitor = LoginMonitor()

    for _ in range(4):
        monitor.record_failure("student@example.com")

    monitor.record_success("student@example.com")

    monitor.record_failure("student@example.com")

    assert monitor.is_locked("student@example.com") is False


def test_identifiers_have_independent_failure_counters():
    monitor = LoginMonitor()

    for _ in range(4):
        monitor.record_failure("student@example.com")

    monitor.record_failure("another@example.com")

    assert monitor.is_locked("student@example.com") is False
    assert monitor.is_locked("another@example.com") is False


def test_identifier_matching_is_case_insensitive():
    monitor = LoginMonitor()

    for _ in range(4):
        monitor.record_failure("Student@example.com")

    monitor.record_failure("STUDENT@example.com")

    assert monitor.is_locked("student@example.com") is True
