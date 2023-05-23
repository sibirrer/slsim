import pytest
from astropy.cosmology import FlatLambdaCDM
from astropy.table import Table
from sim_pipeline.gg_lens import GGLens, image_separation_from_positions, theta_e_when_source_infinity

import os


class TestGGLens(object):
    # pytest.fixture(scope='class')
    def setup_method(self):
        # path = os.path.dirname(sim_pipeline.__file__)

        path = os.path.dirname(__file__)
        module_path, _ = os.path.split(path)
        print(path, module_path)
        blue_one = Table.read(os.path.join(path, 'TestData/blue_one_modified.fits'), format='fits')
        red_one = Table.read(os.path.join(path, 'TestData/red_one_modified.fits'), format='fits')
        cosmo = FlatLambdaCDM(H0=70, Om0=0.3)
        self.source_dict = blue_one
        self.deflector_dict = red_one
        self.gg_lens = GGLens(source_dict=self.source_dict, deflector_dict=self.deflector_dict, cosmo=cosmo)

    def test_deflector_ellipticity(self):
        e1_light, e2_light, e1_mass, e2_mass = self.gg_lens.deflector_ellipticity()
        assert pytest.approx(e1_light, rel=1e-3) == -0.05661955320450283
        assert pytest.approx(e2_light, rel=1e-3) == 0.08738390223219591
        assert pytest.approx(e1_mass, rel=1e-3) == -0.08434700688970058
        assert pytest.approx(e2_mass, rel=1e-3) == 0.09710653297997263

    def test_deflector_magnitude(self):
        band = 'g'
        deflector_magnitude = self.gg_lens.deflector_magnitude(band)
        assert isinstance(deflector_magnitude[0], float)
        assert pytest.approx(deflector_magnitude[0], rel=1e-3) == 26.4515655

    def test_source_magnitude(self):
        band = 'g'
        source_magnitude = self.gg_lens.source_magnitude(band)
        assert pytest.approx(source_magnitude[0], rel=1e-3) == 30.780194

    def test_image_separation_from_positions(self):
        image_positions = self.gg_lens.get_image_positions()
        image_separation = image_separation_from_positions(image_positions)
        theta_E_infinity = theta_e_when_source_infinity(deflector_dict=self.deflector_dict)

        assert image_separation < 2 * theta_E_infinity

    def test_theta_e_when_source_infinity(self):
        theta_E_infinity = theta_e_when_source_infinity(deflector_dict=self.deflector_dict)
        # We expect that theta_E_infinity should be less than 15
        assert theta_E_infinity < 15

if __name__ == '__main__':
    pytest.main()