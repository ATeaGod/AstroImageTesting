import numpy as np
import matplotlib.pyplot as plt
from photutils.aperture import EllipticalAperture
from astropy.io import fits
from astropy.utils.data import download_file
from photutils.isophote import Ellipse, build_ellipse_model

# file stuffs #

filepath = input("FilePath >>> ")
hdu = fits.open(filepath)
data = hdu[0].data
hdu.close()

# Elipse Creation #

ellipse = Ellipse(data)
isolist = ellipse.fit_image(sma0=20.)
print(isolist.to_table())

# Brightness Graph #

plt.figure(figsize=(8, 4))
plt.scatter(isolist.sma**0.25, -2.5*np.log10(isolist.intens))
plt.title("brightness profile")
plt.xlabel('sma**1/4')
plt.ylabel('Magnitude')
plt.gca().invert_yaxis()
plt.show()

# Model Generation #

model_image = build_ellipse_model(data.shape, isolist)

residual = data - model_image

# Final Graph Creation #

figure, axis = plt.subplots(1, 3)
axis[0].imshow(data, origin='lower')
axis[0].set_title("Galaxy")
axis[1].imshow(model_image, origin='lower')
axis[1].set_title("Galaxy Model")
axis[2].imshow(residual, origin='lower')
axis[2].set_title("Residual Image")
plt.show()

# File Saving #

hdu_residual = fits.PrimaryHDU(residual)
hdu_residual.writeto('residual.fits', overwrite=True)
hdu_model = fits.PrimaryHDU(model_image)
hdu_model.writeto('model_image.fits', overwrite=True)
