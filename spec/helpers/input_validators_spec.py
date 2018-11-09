from spec.spec_helper import *
import helpers.input_validators as iv
import argparse

with description(iv) as self:

    with shared_context('number is negative'):
        with it('raises error'):
            expect(
                self.lambda_to_test
            ).to(
                raise_error(argparse.ArgumentTypeError, self.error_message)
            )

    with shared_context('number is positive'):
        with it('returns number'):
            expect(
                self.lambda_to_test()
            ).to(equal(self.output_number))

    with description('#check_inclusion_in_unity'):
        with before.each:
            self.lambda_to_test = lambda: iv.check_inclusion_in_unity(self.input_number)

        with description('0<number<1'):
            with before.all:
                self.input_number = 0.5
                self.output_number = self.input_number
            with included_context('number is positive'):
                pass

        with description('number == 1'):
            with before.all:
                self.input_number = 1
                self.output_number = self.input_number
            with included_context('number is positive'):
                pass

        with description('number == 0'):
            with before.all:
                self.input_number = 0
                self.error_message = "value must be > 0 and <= 1, but your's is %s" % self.input_number

            with included_context('number is negative'):
                pass

        with description('number is negative'):
            with before.all:
                self.input_number = -2.8
                self.error_message = "%s is not a non-negative number" % self.input_number

            with included_context('number is negative'):
                pass

        with description('number > 1'):
            with before.all:
                self.input_number = 3
                self.error_message = "value must be > 0 and <= 1, but your's is %s" % self.input_number

            with included_context('number is negative'):
                pass

    with shared_context('positive int checker'):
        with description('number is positive'):

            with description('value is int'):
                with before.all:
                    self.input_number = 1
                    self.output_number = self.input_number

                with included_context('number is positive'):
                    pass

            with description('value is float'):
                with before.all:
                    self.input_number = 1.4
                    self.output_number = 1

                with included_context('number is positive'):
                    pass

        with description('number is zero'):
            with before.all:
                self.input_number = 0
                self.output_number = self.input_number

            with included_context('number is positive'):
                pass

        with description('number is negative'):

            with shared_context('negative number'):
                with before.all:
                    self.error_message = "%s is not a non-negative number" % self.input_number

                with included_context('number is negative'):
                    pass

            with description('value is int'):
                with before.all:
                    self.input_number = -1

                with included_context('negative number'):
                    pass

            with description('value is float'):
                with before.all:
                    self.input_number = -1.1

                with included_context('negative number'):
                    pass

    with description('#check_positive_int'):
        with before.each:
            self.lambda_to_test = lambda: iv.check_positive_int(self.input_number)

        with included_context('positive int checker'):
            pass

    with shared_context('positive float checker'):
        with description('number is positive'):

            with before.all:
                self.input_number = 1.4
                self.output_number = self.input_number

            with included_context('number is positive'):
                pass

        with description('number is zero'):
            with before.all:
                self.input_number = 0.0
                self.output_number = self.input_number

            with included_context('number is positive'):
                pass

        with description('number is negative'):
            with before.all:
                self.input_number = -1.1
                self.error_message = "%s is not a non-negative number" % self.input_number

            with included_context('number is negative'):
                pass

    with description('#check_positive_float'):
        with before.each:
            self.lambda_to_test = lambda: iv.check_positive_float(self.input_number)

        with included_context('positive float checker'):
            pass

    with description('#check_positive'):
        with description('integer'):
            with before.each:
                self.lambda_to_test = lambda: iv.check_positive(self.input_number, int)

            with included_context('positive int checker'):
                pass

        with description('float'):
            with before.each:
                self.lambda_to_test = lambda: iv.check_positive(self.input_number, float)

            with included_context('positive float checker'):
                pass

    with description('#str2bool'):
        with before.all:
            self.false_values = ('no', 'falSe', 'f', 'N', 'n', '0')
            self.true_values = ('yEs', 'tRue', 'T', 'y', '1', 't')

        with description('False values'):
            with it('returns ƒalse'):
                for val in self.false_values:
                    expect(iv.str2bool(val)).to(be_false)

        with description('True values'):
            with it('returns True'):
                for val in self.true_values:
                    expect(iv.str2bool(val)).to(be_true)

        with description('invalid value'):
            with before.all:
                self.error_message = 'test is not a boolean value, allowed values (case insensitive) for True: yes, true, t, y, 1 and for False: no, false, f, n, 0'

            with it('raises error'):
                expect(
                    lambda: iv.str2bool('test')
                ).to(
                    raise_error(argparse.ArgumentTypeError, self.error_message)
                )