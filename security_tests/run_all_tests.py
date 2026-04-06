from security_tests import tamper_test, replay_test, integrity_test, signature_failure_test


def run_all():
    print("\n===== SECURITY TEST SUITE =====\n")

    print("1. Tampering Test")
    tamper_test.run()

    print("\n2. Replay Attack Test")
    replay_test.run()

    print("\n3. Integrity Attack Test")
    integrity_test.run()

    print("\n4. Signature Failure Test")
    signature_failure_test.run()

    print("\n===== ALL TESTS COMPLETE =====")


if __name__ == "__main__":
    run_all()