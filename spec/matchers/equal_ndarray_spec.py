from spec.spec_helper import *

with description(equal_ndarray) as self:
    with before.each:
        self.matcher = equal_ndarray(self.expected, self.precision)
    with description('#__init__'):
        with before.all:
            self.expected_message_success_precision = ["arrays are equal with precision 2"]
            self.expected_message_failure_precision = ["arrays are not equal with precision 2"]
            self.expected_message_success = ["arrays are equal"]
            self.expected_message_failure = ["arrays are not equal"]

        with description('expected is not an ndarray'):
            with before.all:
                self.expected = [1.333,2.444,3.555]
                self.precision = 2
            with it('sets correct values'):
                expect(
                    self.matcher._original_expected_array
                ).to(
                    equal(self.expected)
                )
                expect(
                    self.matcher._precision
                ).to(
                    equal(self.precision)
                )
                expect(self.matcher).not_to(have_property('_rounded_expected_array'))
                expect(self.matcher).not_to(have_property('_message_success'))
                expect(self.matcher).not_to(have_property('_message_failure'))

        with description('precision is not an integer'):
            with before.all:
                self.expected = np.array([1.333,2.444,3.555])
                self.precision = 'test'
            with it('sets correct values'):
                expect(
                    self.matcher._precision
                ).to(
                    equal(self.precision)
                )
                expect(
                    np.all(self.matcher._original_expected_array == self.expected)
                ).to(
                    equal(True)
                )
                expect(self.matcher).not_to(have_property('_rounded_expected_array'))
                expect(self.matcher).not_to(have_property('_message_success'))
                expect(self.matcher).not_to(have_property('_message_failure'))

        with shared_context('default attributes checker'):
            with it('sets correct values'):
                expect(
                    self.matcher._precision
                ).to(
                    equal(self.precision)
                )
                expect(
                    np.all(self.matcher._original_expected_array == self.expected)
                ).to(
                    equal(True)
                )
                expect(
                    np.all(
                        self.matcher._rounded_expected_array == self.expected
                    )
                ).to(
                    equal(True)
                )

                expect(
                    self.matcher._message_success
                ).to(
                    equal(self.expected_message_success)
                )
                expect(
                    self.matcher._message_failure
                ).to(
                    equal(self.expected_message_failure)
                )

        with description('precision has default value'):
            with before.each:
                self.matcher = equal_ndarray(self.expected)
            with before.all:
                self.expected = np.array([1.333,2.444,3.555])
                self.precision = None
            with included_context('default attributes checker'):
                pass

        with description('precision is None'):
            with before.all:
                self.expected = np.array([1.333,2.444,3.555])
                self.precision = None
            with included_context('default attributes checker'):
                pass

        with description('precision is zero'):
            with before.all:
                self.expected = np.array([1.333,2.444,3.555])
                self.precision = 0
            with it('sets correct values'):
                expect(
                    self.matcher._precision
                ).to(
                    equal(self.precision)
                )
                expect(
                    np.all(
                        self.matcher._rounded_expected_array == np.array([1.0,2.0,4.0])
                    )
                ).to(
                    equal(True)
                )

                expect(
                    self.matcher._message_success
                ).to(
                    equal(["arrays are equal with precision 0"])
                )
                expect(
                    self.matcher._message_failure
                ).to(
                    equal(["arrays are not equal with precision 0"])
                )

        with description('precision is an integer'):
            with before.all:
                self.expected = 'qwerty'
                self.precision = 2
            with it('sets correct values'):
                expect(
                    self.matcher._precision
                ).to(
                    equal(self.precision)
                )
                expect(
                    self.matcher._original_expected_array
                ).to(
                    equal(self.expected)
                )
                expect(self.matcher).not_to(have_property('_rounded_expected_array'))
                expect(self.matcher).not_to(have_property('_message_success'))
                expect(self.matcher).not_to(have_property('_message_failure'))

        with description('expected is and ndarray and precision is an integer'):
            with before.all:
                self.expected = np.array([1.333,2.444,3.555])
                self.precision = 2
            with it('sets correct values'):
                expect(
                    self.matcher._precision
                ).to(
                    equal(self.precision)
                )
                expect(
                    np.all(self.matcher._original_expected_array == self.expected)
                ).to(
                    equal(True)
                )
                expect(
                    np.all(
                        self.matcher._rounded_expected_array == np.array([1.33,2.44,3.56])
                    )
                ).to(
                    equal(True)
                )

                expect(
                    self.matcher._message_success
                ).to(
                    equal(self.expected_message_success_precision)
                )
                expect(
                    self.matcher._message_failure
                ).to(
                    equal(self.expected_message_failure_precision)
                )

    with description('#_match'):
        with before.each:
            self.actual_result = self.matcher._match(self.actual)
        with description('expected is not an ndarray'):
            with before.all:
                self.expected = [1.333,2.444,3.555]
                self.precision = 2
                self.actual = np.array([1.333,2.444,3.555])
            with it('returns False with message'):
                expect(
                    self.actual_result
                ).to(
                    equal((False, ['expected was not an ndarray']))
                )
        with description('precision is not an integer'):
            with before.all:
                self.expected = np.array([1.333,2.444,3.555])
                self.precision = 'qwerty'
                self.actual = np.array([1.333,2.444,3.555])
            with it('returns False with message'):
                expect(
                    self.actual_result
                ).to(
                    equal((False, ['precision was not an integer']))
                )

        with shared_context('comparer with default precision'):
            with description('expected and actual are equal'):
                with before.all:
                   self.expected = np.array([1.333,2.444,3.555])
                   self.precision = None
                   self.actual = np.array([1.333,2.444,3.555])
                with it('returns True with message'):
                   expect(
                       self.actual_result
                   ).to(
                       equal((True, ['arrays are equal']))
                   )
            with description('expected and actual are not equal'):
                with before.all:
                   self.expected = np.array([1.333,2.444,3.555])
                   self.precision = None
                   self.actual = np.array([1.33,2.44,3.56])
                with it('returns True with message'):
                   expect(
                       self.actual_result
                   ).to(
                       equal((False, ['arrays are not equal']))
                   )
            with description('expected and actual have different shapes'):
                with before.all:
                   self.expected = np.array([1.333,2.444,3.555]).reshape((-1,1))
                   self.precision = None
                   self.actual = np.array([1.333,2.444,3.555])
                with it('returns True with message'):
                   expect(
                       self.actual_result
                   ).to(
                       equal((False, ['arrays are not equal']))
                   )

        with description('precision has default value'):
            with before.each:
                self.matcher = equal_ndarray(self.expected)
            with before.all:
               self.expected = np.array([1.333,2.444,3.555])
               self.precision = None
               self.actual = np.array([1.333,2.444,3.555])
            with included_context('comparer with default precision'):
                pass

        with description('precision is None'):
            with before.all:
               self.expected = np.array([1.333,2.444,3.555])
               self.precision = None
               self.actual = np.array([1.333,2.444,3.555])
            with included_context('comparer with default precision'):
                pass

        with description('precision is integer'):
            with description('arrays are equal within precision'):
                with before.all:
                    self.expected = np.array([1.333,2.444,3.555])
                    self.precision = 2
                    self.actual = np.array([1.33,2.44,3.56])
                with it('returns True with message'):
                    expect(
                        self.actual_result
                    ).to(
                        equal((True, ['arrays are equal with precision 2']))
                    )

            with description('arrays are equal'):
                with before.all:
                    self.expected = np.array([1.33,2.44,3.56])
                    self.precision = 2
                    self.actual = np.array([1.33,2.44,3.56])
                with it('returns True with message'):
                    expect(
                        self.actual_result
                    ).to(
                        equal((True, ['arrays are equal with precision 2']))
                    )

            with description('arrays are not equal within precision'):
                with before.all:
                    self.expected = np.array([1.33,2.44,3.56])
                    self.precision = 2
                    self.actual = np.array([1.33,2.44,3.55])
                with it('returns True with message'):
                    expect(
                        self.actual_result
                    ).to(
                        equal((False, ['arrays are not equal with precision 2']))
                    )

    with description('#__repr__'):
        with description('precision is None'):
            with before.all:
                self.expected = np.array([1.33,2.44,3.56])
                self.precision = None
            with it('returns correct value'):
                expect(
                    self.matcher.__repr__()
                ).to(
                    equal('equal')
                )
        with description('precision is default'):
            with before.each:
                self.matcher = equal_ndarray(self.expected)
            with before.all:
                self.expected = np.array([1.33,2.44,3.56])
                self.precision = None
            with it('returns correct value'):
                expect(
                    self.matcher.__repr__()
                ).to(
                    equal('equal')
                )
        with description('precision is not None'):
            with before.all:
                self.expected = np.array([1.33,2.44,3.56])
                self.precision = 2
            with it('returns correct value'):
                expect(
                    self.matcher.__repr__()
                ).to(
                    equal('equal with precision 2')
                )