from spec.spec_helper import *
import clean.restorer as rst
import clean.matrix_builder as mb

with description(rst.Restorer) as self:
    with before.all:
        pass

    with before.each:
        pass

    with description('__init__'):
        with it('sets all values'):
            pass