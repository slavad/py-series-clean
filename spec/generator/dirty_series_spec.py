from spec.spec_helper import *
import generator.dirty_series as ds

#TODO split into files using shared contexts
#TODO refactor to remove duplications using before blocks
with description(ds.DirtySeries) as self:
    with before.all:
      self.time_grid_length = 10
      self.max_time_value = 20
      self.frequencies = np.array([0.1, 0.2]) # linear frequencies!
      self.amplitudes = np.array([10, 20])
      self.phases = np.array([0.4, 0.6])
      self.sigma = 1
      self.round_precision = 8

    with before.each:
        self.generator = ds.DirtySeries(
            self.time_grid_length, self.max_time_value,
            self.frequencies, self.amplitudes,
            self.phases, self.sigma
        )
    with description('#__init__'):
        with description('incorrect argument shapes (amplitude)'):
            with before.each:
                amplitudes = np.array([10])
                self.action = lambda: ds.DirtySeries(
                    self.time_grid_length, self.max_time_value,
                    self.frequencies, amplitudes,
                    self.phases, self.sigma
                )
            with it('raises error'):
                expect(self.action).to(raise_error(ValueError))
        with description('correct arguments'):
            with it('sets all values'):
                expect(
                    self.time_grid_length
                ).to(
                    equal(self.generator._DirtySeries__time_grid_length)
                )
                expect(
                    self.max_time_value
                ).to(
                    equal(self.generator._DirtySeries__max_time_value)
                )
                expect(
                    np.all(
                        np.array(
                            [[0.1],[0.2]]
                        ) == self.generator._DirtySeries__frequnecies
                    )
                ).to(
                    equal(True)
                )
                expect(
                    np.all(
                        np.array(
                            [[10],[20]]
                        ) == self.generator._DirtySeries__amplitudes
                    )
                ).to(
                    equal(True)
                )
                expect(
                    np.all(
                        np.array(
                            [[0.4],[0.6]]
                        ) == self.generator._DirtySeries__phases
                    )
                ).to(
                    equal(True)
                )
                expect(
                    self.sigma
                ).to(
                    equal(self.generator._DirtySeries__sigma)
                )

    with description('#generate'):
        with before.each:
            self.result = self.generator.generate()
            self.time_grid = self.result[0]
            self.dirty_periodical_series = self.result[1]
            self.clean_periodical_series = self.generator._DirtySeries__generate_periodical_series(
                self.time_grid
            )
        with description('sigma is zero'):
            with before.all:
                self.sigma = 0
            with it('does not add noise'):
                expect(
                    np.all(
                        self.dirty_periodical_series == self.clean_periodical_series
                    )
                ).to(
                    equal(True)
                )

        with description('sigma is not zero'):
            with before.all:
                self.sigma = 1
            with it('adds noise'):
                expect(
                    np.all(
                        self.dirty_periodical_series == self.clean_periodical_series
                    )
                ).to(
                    equal(False)
                )
        with it('generates result of the correct length'):
            expect(len(self.result)).to(equal(2))

        with it('generates series of desired length'):
            expect(self.time_grid.shape).to(
                equal((self.time_grid_length, 1))
            )

        with it('always generates different time grid'):
            new_time_grid = self.generator.generate()[0]
            expect(
                np.all(
                    self.time_grid == new_time_grid
                )
            ).to(
                equal(False)
            )

    with description('#__check_and_reshape_arguments'):
        with before.each:
            self.action = lambda: self.generator._DirtySeries__check_and_reshape_arguments(
                self.old_freq, self.old_amp, self.old_phase
            )
        with description('inputs are valud'):
            with description('all are scalars'):
                with before.all:
                    self.old_freq = 1
                    self.old_amp = 2
                    self.old_phase = 3
                with it('returns matrices'):
                    freq, amp, phase = self.action()
                    expect(
                        freq
                    ).to(
                        equal(np.array([[1]]))
                    )
                    expect(
                        amp
                    ).to(
                        equal(np.array([[2]]))
                    )
                    expect(
                        phase
                    ).to(
                        equal(np.array([[3]]))
                    )

            with description('all are vectors of the same size'):
                with before.all:
                    self.old_freq = np.array([3, 2])
                    self.old_amp = np.array([0.4, 0.6])
                    self.old_phase = np.array([4, 6])
                with it('returns reshaped matrices'):
                    freq, amp, phase = self.action()
                    expect(
                        np.all(
                            freq == np.array([[3],[2]])
                        )
                    ).to(
                        equal(True)
                    )
                    expect(
                        np.all(
                            amp == np.array([[0.4],[0.6]])
                        )
                    ).to(
                        equal(True)
                    )
                    expect(
                        np.all(
                            phase == np.array([[4],[6]])
                        )
                    ).to(
                        equal(True)
                    )
            with description('one scalar, other are vectors of size 1'):
                with it('returns matrices'):
                    with before.all:
                        self.old_freq = 1
                        self.old_amp = np.array([2])
                        self.old_phase = np.array([3])
                    with it('returns matrices'):
                        freq, amp, phase = self.action()
                        expect(
                            freq
                        ).to(
                            equal(np.array([[1]]))
                        )
                        expect(
                            amp
                        ).to(
                            equal(np.array([[2]]))
                        )
                        expect(
                            phase
                        ).to(
                            equal(np.array([[3]]))
                        )

        with description('inputs are not valid'):
            with description('one scalar, other are vectors of size > 2'):
                with before.all:
                    self.old_freq = 1
                    self.old_amp = np.array([0.4, 0.6])
                    self.old_phase = np.array([4, 6])

                with it('raises error'):
                    expect(self.action).to(raise_error(ValueError))

            with description('frequencies shape is different from others'):
                with before.all:
                    self.old_freq = np.array([0.4, 0.6, 1])
                    self.old_amp = np.array([0.4, 0.6])
                    self.old_phase = np.array([4, 6])

                with it('raises error'):
                    expect(self.action).to(raise_error(ValueError))

            with description('amplitudes shape is different from others'):
                with before.all:
                    self.old_freq = np.array([0.4, 0.6])
                    self.old_amp = np.array([0.4, 0.6, 1])
                    self.old_phase = np.array([4, 6])

                with it('raises error'):
                    expect(self.action).to(raise_error(ValueError))

            with description('phases amplitude shape is different from others'):
                with before.all:
                    self.old_freq = np.array([0.4, 0.6, 1])
                    self.old_amp = np.array([0.4, 0.6])
                    self.old_phase = np.array([4, 6, 1])

                with it('raises error'):
                    expect(self.action).to(raise_error(ValueError))

    with description('#__reshape_one_value'):
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

    with description('#__generate_random_time_grid'):
        with before.each:
            self.time_grid = self.generator._DirtySeries__generate_random_time_grid()
        with it('time grid starts with desired value'):
            expect(self.time_grid[0][0]).to(be_above_or_equal(0))
            expect(self.time_grid[0][0]).to(be_below(self.max_time_value))

        with it('time grid ends with desired value'):
            expect(self.time_grid[0][0]).to(be_below_or_equal(self.max_time_value))

        with it('time grid has correct shape'):
            expect(self.time_grid.shape).to(equal((self.time_grid_length, 1)))
        with it('grid is always different'):
            new_grid = self.generator._DirtySeries__generate_random_time_grid()
            expect(
                np.all(
                    new_grid == self.time_grid
                )
            ).to(
                equal(False)
            )

    with shared_context('resulting series checker'):
        with before.each:
            self.periodical_series = np.around(
                self.generator._DirtySeries__generate_periodical_series(self.time_grid), self.round_precision
            )

        with description('single harmonic'):
            with it('returns correct result'):
                expect(
                    np.all(
                        self.periodical_series == self.expected_periodical_series
                    )
                ).to(
                    equal(True)
                )

    with description('#__generate_periodical_series'):
        with description('simple time grid and one harmonic'):
            with before.all:
              self.frequencies = np.array([2.0]) # linear frequencies!
              self.phases = np.array([0.0])
              self.amplitudes = np.array([20.0])
              self.time_grid = np.array(
                  [
                      0,
                      0.125,
                      0.25,
                      0.375,
                      0.5,
                      0.625,
                      0.75,
                      0.875,
                      1.0
                  ]
              )
              self.expected_periodical_series = np.array(
                  [
                      self.amplitudes[0], 0,
                      -self.amplitudes[0], 0,
                      self.amplitudes[0],0,
                      -self.amplitudes[0], 0,
                      self.amplitudes[0]
                  ]
              ).reshape((-1,1))
            with included_context('resulting series checker'):
                pass
        with description('one harmonic, with non-zero phase'):
          with before.all:
            self.frequencies = np.array([1.0]) # linear frequencies!
            self.phases = np.array([0.3])
            self.amplitudes = np.array([20.0])
            self.time_grid = np.array(
                [
                    0-self.phases[0]/(2*np.pi),
                    0.25-self.phases[0]/(2*np.pi),
                    0.5-self.phases[0]/(2*np.pi),
                    0.75-self.phases[0]/(2*np.pi),
                    1.0-self.phases[0]/(2*np.pi),
                ]
            )
            self.expected_periodical_series = np.array(
                [
                    self.amplitudes[0], 0,
                    -self.amplitudes[0], 0,
                    self.amplitudes[0]
                ]
            ).reshape((-1,1))
          with included_context('resulting series checker'):
              pass
        with description('two harmoincs, resonance phases'):
            with before.all:
              self.frequencies = np.array([1.0, 2.0]) # linear frequencies!
              self.phases = np.array([0.0, np.pi])
              self.amplitudes = np.array([20.0, 10.0])
              self.time_grid = np.array(
                  [
                      0,
                      0.25,
                      0.5,
                      0.75,
                      1.0
                  ]
              )
              self.expected_periodical_series = np.array(
                  [
                      self.amplitudes[0] - self.amplitudes[1],
                      self.amplitudes[1],
                      -self.amplitudes[0] - self.amplitudes[1],
                      self.amplitudes[1],
                      self.amplitudes[0] - self.amplitudes[1]
                  ]
              ).reshape((-1,1))
            with included_context('resulting series checker'):
                pass

        with description('two harmoincs, non-resonance phases'):
            with before.all:
              self.frequencies = np.array([1.0, 2.0]) # linear frequencies!
              self.phases = np.array([0.3, 0.2])
              self.amplitudes = np.array([20.0, 10.0])
              self.time_grid = np.array(
                  [
                      0,
                      0.25,
                      0.5,
                      0.75,
                      1.0
                  ]
              )
              self.expected_periodical_series = np.array(
                  [
                      28.90739556,
                      -15.71106991,
                      -9.306064,
                      -3.89026165,
                      28.90739556
                  ]
              ).reshape((-1,1))
            with included_context('resulting series checker'):
                pass

    with description('#__generate_noise'):
        with before.each:
            self.shape = (10000,1)
            self.noise = self.generator._DirtySeries__generate_noise(
                self.shape
            )
        with it('has correct shape'):
            expect(self.noise.shape).to(equal(self.shape))

        with it('is always different'):
            new_noise = self.generator._DirtySeries__generate_noise(
                self.shape
            )
            expect(
                np.all(
                    new_noise == self.noise
                )

            ).to(
                equal(False)
            )
        with it('has approx zero mean'):
            expect(np.around(np.mean(self.noise), -2)).to(equal(0.0))
    with description('#__generate_dirty_periodical_series'):
        with before.all:
          self.frequencies = np.array([1.0]) # linear frequencies!
          self.phases = np.array([0.0])
          self.amplitudes = np.array([20.0])
          self.time_grid = np.array(
              [
                  0,
                  0.25,
                  0.5,
                  0.75,
                  1.0
              ]
          )
          self.clean_periodical_series = np.array(
              [
                  self.amplitudes[0], 0,
                  -self.amplitudes[0], 0,
                  self.amplitudes[0]
              ]
          ).reshape((-1,1))
        with description('sigma is zero'):
            with before.each:
                self.sigma = 0
                self.generator = ds.DirtySeries(
                    self.time_grid_length, self.max_time_value,
                    self.frequencies, self.amplitudes,
                    self.phases, self.sigma
                )
                self.dirty_periodical_series = np.around(
                    self.generator._DirtySeries__generate_dirty_periodical_series(self.time_grid), self.round_precision
                )
            with it('does not add noise'):
                expect(
                    np.all(
                        self.clean_periodical_series == self.dirty_periodical_series
                    )
                ).to(
                    equal(True)
                )
        with description('sigma is not zero'):
            with before.each:
                self.sigma = 1
                self.generator = ds.DirtySeries(
                    self.time_grid_length, self.max_time_value,
                    self.frequencies, self.amplitudes,
                    self.phases, self.sigma
                )
                self.dirty_periodical_series = np.around(
                    self.generator._DirtySeries__generate_dirty_periodical_series(self.time_grid), self.round_precision
                )
            with it('adds noise'):
                expect(
                    np.all(
                        self.clean_periodical_series == self.dirty_periodical_series
                    )
                ).to(
                    equal(False)
                )
            with it('noise is always different'):
                new_dirty_periodical_series = np.around(
                    self.generator._DirtySeries__generate_dirty_periodical_series(self.time_grid), self.round_precision
                )
                expect(
                    np.all(
                        new_dirty_periodical_series == self.dirty_periodical_series
                    )
                ).to(
                    equal(False)
                )
