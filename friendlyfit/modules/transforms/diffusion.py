from math import isnan

import numexpr as ne
import numpy as np

from ...constants import C_CGS, DAY_CGS, FOUR_PI, KM_CGS, M_SUN_CGS
from ..module import Module

CLASS_NAME = 'Diffusion'


class Diffusion(Module):
    """Diffusion transform.
    """

    N_INT_TIMES = 20
    MIN_EXP_ARG = 10

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def process(self, **kwargs):
        self._t_explosion = kwargs['texplosion']
        self._kappa = kwargs['kappa']
        self._kappa_gamma = kwargs['kappagamma']
        self._m_ejecta = kwargs['mejecta']
        self._v_ejecta = kwargs['vejecta']
        self._times = kwargs['times']
        self._luminosities = kwargs['luminosities']
        self._times_since_exp = [(x - self._t_explosion) * DAY_CGS
                                 for x in self._times]
        self._tau_diff = np.sqrt(2.0 * self._kappa * self._m_ejecta * M_SUN_CGS
                                 / (13.7 * C_CGS * (self._v_ejecta * KM_CGS)))
        self._trap_coeff = (3.0 * self._kappa_gamma * self._m_ejecta *
                            M_SUN_CGS / (FOUR_PI *
                                         (self._v_ejecta * KM_CGS)**2))
        td, A = self._tau_diff, self._trap_coeff

        new_lum = []
        for te in self._times_since_exp:
            if te <= 0.0:
                new_lum.append(0.0)
                continue
            tb = np.sqrt(max(te**2 - (self.MIN_EXP_ARG * td)**2, 0.0))
            int_times = np.linspace(tb, te, self.N_INT_TIMES)
            int_lums = np.interp(int_times, self._times_since_exp,
                                 self._luminosities)
            int_arg = ne.evaluate('2.0 * int_lums * int_times / td**2 * '
                                  'exp((int_times**2 - te**2) / td**2) * '
                                  '(1.0 - exp(-A / te**2))')
            # int_arg = [
            #     2.0 * l * t / td**2 *
            #     np.exp((t**2 - te**2) / td**2) * (1.0 - np.exp(-A / te**2))
            #     for t, l in zip(int_times, int_lums)
            # ]
            int_arg = [0.0 if isnan(x) else x for x in int_arg]
            new_lum.append(np.trapz(int_arg, int_times))
        return {'luminosities': new_lum}
