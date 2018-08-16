from spec.spec_helper import *
import generator.dirty_series as ds

with description(ds.DirtySeries) as self:
    with before.all:
      self.time_grid_length = 10
      self.max_time_value = 20
      self.frequencies = np.array([0.1, 0.2])
      self.phases = np.array([0.4, 0.6])
      self.amplitudes = np.array([10, 20])
      self.sigma = 1
    with before.each:
        self.generator = ds.DirtySeries(
            self.time_grid_length, self.max_time_value,
            self.frequencies, self.phases,
            self.amplitudes, self.sigma
        )
    with description('DirtySeries#__reshape_one_value'):
        with it('converts scalar to array'):
            expect(
                self.generator._DirtySeries__reshape_one_value(1)
            ).to(
                equal(np.array([[1]]))
            )
        with it('reshapes 1d array'):
            expect(
                np.all(
                    self.generator._DirtySeries__reshape_one_value(
                        np.array([1,2])
                    ) == np.array([[1],[2]])
                )
            ).to(
                equal(True)
            )
