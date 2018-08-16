from mamba import description, context, it
from expects import expect, equal
import generator.dirty_series as ds

with description(ds.DirtySeries) as self:
    with description('DirtySeries#__reshape_one_value'):
        with it('converts scalar to array'):
            expect(1).to(equal(1))
