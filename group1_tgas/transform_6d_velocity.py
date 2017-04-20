from astropy.table import Table, join, Column
from convert_gal_movement import *

rave_dr5 = Table.read('RAVE_DR5.fits')
rave_tgas = Table.read('RAVE_TGAS.fits')
# rename one of the cols, because the distance was calculated using stellar parameters
rave_dr5['parallax'].name = 'parallax_binney'

rave_tgas_data = join(rave_dr5, rave_tgas, keys='RAVE_OBS_ID')

# compute galactic cilindrical velocities u, v and w
u,v,w = gal_uvw(rave_tgas_data['ra'], rave_tgas_data['dec'], rave_tgas_data['pmra'],
                rave_tgas_data['pmdec'], rave_tgas_data['HRV'], rave_tgas_data['parallax'], lsr=False)

# description of velocity vector
# The components of space velocity in the Milky Way's Galactic coordinate system are usually designated
# U, V, and W, given in km/s, with U positive in the direction of the Galactic Center, V positive in the
# direction of galactic rotation, and W positive in the direction of the North Galactic Pole.

data_out = rave_tgas_data['RAVE_OBS_ID', 'ra', 'dec', 'parallax', 'pmra', 'pmdec', 'HRV']
data_out.add_column(Column(data=u, name='gal_u', dtype=np.float64))
data_out.add_column(Column(data=v, name='gal_v', dtype=np.float64))
data_out.add_column(Column(data=w, name='gal_w', dtype=np.float64))

data_out.write('tgas_rave_velocity.fits')
