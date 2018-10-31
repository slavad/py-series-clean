from spec.spec_helper import *

with description(equal_with_precision) as self:
    with before.each:
        self.matcher = equal_with_precision(self.expected, self.precision)

    with description('#__init__'):
        with before.all:
            self.expected = 1.333
            self.precision = 2
        with it('sets values'):
            expect(
                self.matcher._precision
            ).to(
                equal(self.precision)
            )
            expect(
                self.matcher._original_expected_number
            ).to(
                equal(self.expected)
            )
    with description('#_match'):
        with description('invalid input'):
            with before.each:
                self.action = lambda: self.matcher._match(self.actual)

            with description('expected is not a number'):
                with before.all:
                    self.expected = '1.333'
                    self.precision = 2
                    self.actual = 1.33

                with it('raises error'):
                    expect(self.action).to(
                        raise_error(ValueError, 'expected was not a number')
                    )

            with description('actual is not a number'):
                with before.all:
                    self.expected = 1.333
                    self.precision = 2
                    self.actual = '1.331'

                with it('raises error'):
                    expect(self.action).to(
                        raise_error(ValueError, 'actual was not a number')
                    )

            with description('precision is not a number'):
                with before.all:
                    self.expected = 1.333
                    self.precision = '2'
                    self.actual = 1.33

                with it('raises error'):
                    expect(self.action).to(
                        raise_error(ValueError, 'precision was not an integer')
                    )
        with description('valid input'):
            with before.each:
                self.result = self.matcher._match(self.actual)
            with description('actual and expected are not equal within precision'):
                with before.all:
                    self.expected = 1.333
                    self.precision = 2
                    self.actual = 1.351

                with it('returns False and a message'):
                    expect(self.result).to(
                        equal(
                            (False, ['numbers are not equal with precision 2'])
                        )
                    )

            with description('actual and expected are equal within precision'):
                with before.all:
                    self.expected = 1.333
                    self.precision = 2
                    self.actual = 1.331

                with it('returns True and a message'):
                    expect(self.result).to(
                        equal(
                            (True, ['numbers are equal with precision 2'])
                        )
                    )

            with description('actual and expected are equal within zero precision'):
                with before.all:
                    self.expected = 1.03
                    self.precision = 0
                    self.actual = 1.04

                with it('returns True and a message'):
                    expect(self.result).to(
                        equal(
                            (True, ['numbers are equal with precision 0'])
                        )
                    )

            with description('actual and expected are exactly equal'):
                with before.all:
                    self.expected = 1.33
                    self.precision = 2
                    self.actual = 1.33

                with it('returns True and a message'):
                    expect(self.result).to(
                        equal(
                            (True, ['numbers are equal with precision 2'])
                        )
                    )

    with description('#__repr__'):
        with before.all:
            self.expected = 1.333
            self.precision = 2
        with it('returns correct value'):
            expect(self.matcher.__repr__()).to(equal('equal with precision 2'))

    with description('failure message methods'):
        with before.all:
            self.expected = 1.333
            self.precision = 2
            self.subject = 'subject'
            self.reasons = ['one', 'two']
            self.negated_expected_message = '\nexpected: subject not to equal with precision 2 to 1.333\n     but: one\n          two'
            self.expected_message = '\nexpected: subject to equal with precision 2 to 1.333\n     but: one\n          two'

        with description('#_failure_message_general'):
            with before.each:
                self.message = self.matcher._failure_message_general(self.subject, self.reasons, self.negated)
            with description('negated is True'):
                with before.all:
                    self.negated = True
                with it('returns correct message'):
                    expect(
                        self.message
                    ).to(
                        equal(self.negated_expected_message)
                    )

            with description('negated is False'):
                with before.all:
                    self.negated = False
                with it('returns correct message'):
                    expect(
                        self.message
                    ).to(
                        equal(self.expected_message)
                    )

        with description('#_failure_message'):
            with it('returns correct message'):
                expect(
                    self.matcher._failure_message(self.subject, self.reasons)
                ).to(
                    equal(self.expected_message)
                )

        with description('#_failure_message_negated'):
            with it('returns correct message'):
                expect(
                    self.matcher._failure_message_negated(self.subject, self.reasons)
                ).to(
                    equal(self.negated_expected_message)
                )