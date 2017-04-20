import numpy as np
import astropy.coordinates as coord
import astropy.units as un

from astropy.table import Table, join, Column

tgas_data = Table.read('tgas.fits')

# convert ra, dec and parallax to galactocentric cartesian coordinates
coordinates = coord.ICRS(ra=tgas_data['ra'].data * un.deg,
                         dec=tgas_data['dec'].data * un.deg,
                         distance=1./tgas_data['parallax'].data * un.kpc)
galactocentric = coordinates.transform_to(coord.Galactocentric)

# convert cartesian to spherical
r = np.sqrt(galactocentric.x.value**2 + galactocentric.y.value**2 + galactocentric.z.value**2)
delta = np.rad2deg(np.arccos(galactocentric.z.value/r))
phi = np.rad2deg(np.arctan(galactocentric.y.value, galactocentric.x.value)) + 180.  # to be in range from 0 to 360

# create output data set
data_out = tgas_data['source_id', 'tycho2_id', 'ra', 'dec', 'parallax']
data_out.add_column(Column(data=galactocentric.x.value, name='gal_x', dtype=np.float64))
data_out.add_column(Column(data=galactocentric.y.value, name='gal_y', dtype=np.float64))
data_out.add_column(Column(data=galactocentric.z.value, name='gal_z', dtype=np.float64))
data_out.add_column(Column(data=r, name='gal_r', dtype=np.float64))
data_out.add_column(Column(data=delta, name='gal_delta', dtype=np.float64))
data_out.add_column(Column(data=phi, name='gal_phi', dtype=np.float64))

data_out.write('tgas_coordinates.fits')