from spec.spec_helper import *

with description(have_only_keys) as self:
    with before.all:
        self.actual = ['one', 'two', 'three']

    with before.each:
        self.matcher = have_only_keys(*self.actual)
        self.result = self.matcher._match(self.subject)

    with description('expected is not a dict'):
        with before.all:
            self.subject = 1

        with it('returns False and a message'):
            expect(self.result).to(
                equal(
                    (False, ['is not a dict'])
                )
            )

    with description('subject is a dict'):
        with description('subject and expected keys match exactly'):
            with before.all:
                self.subject = { 'one': 1, 'two': 2, 'three': 3 }
            with it('returns True and a message'):
                expect(self.result).to(
                    equal(
                        (True, ["key 'one' found", "key 'two' found", "key 'three' found"])
                    )
                )

        with description('subject has more keys than expected'):
            with before.all:
                self.subject = { 'one': 1, 'two': 2, 'three': 3, 'four': 4 }
            with it('returns False and a message'):
                expect(self.result).to(
                    equal(
                        (False, ["key 'one' found", "key 'two' found", "key 'three' found", 'keys do not match'])
                    )
                )


        with description('subject has less keys than expected'):
            with before.all:
                self.subject = { 'one': 1, 'two': 2}
            with it('returns False and a message'):
                expect(self.result).to(
                    equal(
                        (False, ["key 'three' not found", 'keys do not match'])
                    )
                )