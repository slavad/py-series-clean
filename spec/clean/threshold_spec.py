from spec.spec_helper import *
import clean.threshold as thrs

with description(thrs.Threshold) as self:
    with description('#__init__'):
        with it('sets all values'):
            pass