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